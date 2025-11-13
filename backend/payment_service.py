from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionResponse, CheckoutStatusResponse, CheckoutSessionRequest
import os
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class PaymentService:
    def __init__(self, host_url: str):
        self.api_key = os.environ.get('STRIPE_API_KEY', 'sk_test_emergent')
        self.host_url = host_url.rstrip('/')
        self.webhook_url = f"{self.host_url}/api/webhook/stripe"
        self.stripe_checkout = StripeCheckout(api_key=self.api_key, webhook_url=self.webhook_url)
        
    async def create_checkout_session(self, 
                                     amount: float, 
                                     currency: str,
                                     metadata: Optional[Dict[str, str]] = None,
                                     frontend_origin: str = None) -> CheckoutSessionResponse:
        """
        Create a Stripe checkout session for custom amount.
        
        Args:
            amount: Payment amount (float, e.g., 100.00)
            currency: Currency code (e.g., 'usd')
            metadata: Additional metadata
            frontend_origin: Frontend URL origin for redirect
            
        Returns:
            CheckoutSessionResponse with checkout URL and session ID
        """
        try:
            # Use frontend_origin if provided, otherwise use host_url
            base_url = frontend_origin if frontend_origin else self.host_url
            
            # Create success and cancel URLs
            success_url = f"{base_url}/success?session_id={{{{CHECKOUT_SESSION_ID}}}}"
            cancel_url = f"{base_url}/booking"
            
            # Create checkout request
            checkout_request = CheckoutSessionRequest(
                amount=float(amount),
                currency=currency,
                success_url=success_url,
                cancel_url=cancel_url,
                metadata=metadata or {}
            )
            
            # Create session via Stripe
            session = await self.stripe_checkout.create_checkout_session(checkout_request)
            
            logger.info(f"Checkout session created: {session.session_id}")
            return session
            
        except Exception as e:
            logger.error(f"Error creating checkout session: {str(e)}")
            raise
    
    async def get_checkout_status(self, session_id: str) -> CheckoutStatusResponse:
        """
        Get the status of a checkout session.
        
        Args:
            session_id: Stripe checkout session ID
            
        Returns:
            CheckoutStatusResponse with payment status
        """
        try:
            status = await self.stripe_checkout.get_checkout_status(session_id)
            logger.info(f"Checkout status retrieved for session {session_id}: {status.payment_status}")
            return status
        except Exception as e:
            logger.error(f"Error retrieving checkout status: {str(e)}")
            raise
    
    async def handle_webhook(self, body: bytes, signature: str) -> dict:
        """
        Handle Stripe webhook events.
        
        Args:
            body: Raw request body as bytes
            signature: Stripe signature from headers
            
        Returns:
            Dictionary with webhook response
        """
        try:
            webhook_response = await self.stripe_checkout.handle_webhook(body, signature)
            logger.info(f"Webhook processed: {webhook_response.event_type}")
            return {
                "event_type": webhook_response.event_type,
                "event_id": webhook_response.event_id,
                "session_id": webhook_response.session_id,
                "payment_status": webhook_response.payment_status,
                "metadata": webhook_response.metadata
            }
        except Exception as e:
            logger.error(f"Error handling webhook: {str(e)}")
            raise

# Service packages with fixed prices
SERVICE_PACKAGES = {
    "vehicle-wrap-deposit": {"amount": 500.00, "name": "Vehicle Wrap Deposit", "currency": "usd"},
    "window-tint-deposit": {"amount": 200.00, "name": "Window Tint Deposit", "currency": "usd"},
    "custom-decals-deposit": {"amount": 150.00, "name": "Custom Decals Deposit", "currency": "usd"},
    "consultation-fee": {"amount": 50.00, "name": "Consultation Fee", "currency": "usd"},
}

def get_package_amount(package_id: str) -> float:
    """
    Get the amount for a service package.
    Security: Never accept amounts from frontend.
    """
    if package_id not in SERVICE_PACKAGES:
        raise ValueError(f"Invalid package ID: {package_id}")
    return SERVICE_PACKAGES[package_id]["amount"]

def get_package_currency(package_id: str) -> str:
    """
    Get the currency for a service package.
    """
    if package_id not in SERVICE_PACKAGES:
        raise ValueError(f"Invalid package ID: {package_id}")
    return SERVICE_PACKAGES[package_id]["currency"]
