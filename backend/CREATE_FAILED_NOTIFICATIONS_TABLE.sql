-- ============================================================================
-- Failed Notifications Table for Optimus Design & Customs
-- This table logs when email notifications fail, so you can review them later
-- Run this SQL in your Supabase SQL Editor
-- ============================================================================

-- Create failed_notifications table
CREATE TABLE IF NOT EXISTS failed_notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    appointment_id UUID NOT NULL,
    recipient_email TEXT NOT NULL,
    appointment_details JSONB NOT NULL,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'failed',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_failed_notifications_created_at ON failed_notifications(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_failed_notifications_status ON failed_notifications(status);
CREATE INDEX IF NOT EXISTS idx_failed_notifications_appointment_id ON failed_notifications(appointment_id);

-- Enable Row Level Security
ALTER TABLE failed_notifications ENABLE ROW LEVEL SECURITY;

-- Create policy to allow service role to do everything
CREATE POLICY "Service role can do everything" ON failed_notifications
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Comment on table
COMMENT ON TABLE failed_notifications IS 'Logs failed email notifications so owner can review missed appointment alerts';

-- Verify table was created
SELECT 'failed_notifications table created successfully!' as status;

-- ============================================================================
-- How to Use This Table:
-- ============================================================================
-- 
-- 1. When an email fails to send, the system automatically logs it here
-- 2. Check this table regularly for any failed notifications
-- 3. The appointment_details field contains all the customer info
-- 4. You can manually contact customers from this data
-- 5. Once resolved, update the resolved_at timestamp
--
-- Example query to see all failed notifications:
-- SELECT * FROM failed_notifications WHERE status = 'failed' ORDER BY created_at DESC;
--
-- Example to mark as resolved:
-- UPDATE failed_notifications SET status = 'resolved', resolved_at = NOW() WHERE id = 'your-id-here';
-- ============================================================================
