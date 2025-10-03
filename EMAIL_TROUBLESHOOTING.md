# Email Functionality Troubleshooting Guide

## ✅ Complete Setup Checklist

### Step 1: Install Required Packages
```bash
pip install sendgrid python-dotenv
```

### Step 2: Verify Installation
```bash
pip list | grep sendgrid
pip list | grep python-dotenv
```

Expected output:
```
sendgrid     6.x.x
python-dotenv 1.x.x
```

### Step 3: Test Email Configuration
```bash
python email_sender.py
```

Expected output:
```
Email Configuration Test
==================================================
Configured: True
API Key: ***ObA
From Email: agovil@aurigincm.com
From Name: Aurigin Trade Processing
==================================================

Email sending enabled: True
```

### Step 4: Start Streamlit and Check UI
```bash
streamlit run unified-streamlit-app.py
```

In the sidebar, you should see:
```
📧 Email Notifications
✓ Email configured
☐ Send email on completion
✅ Default: operations@aurigincm.com
Additional Recipients (optional): [text field]
📧 Total: 1 recipient(s)
```

## 🐛 Common Issues and Solutions

### Issue 1: "Email not available" in UI

**Symptoms:**
- Sidebar shows: "⚠️ Email not available"
- No checkbox to enable email

**Cause:** sendgrid package not installed

**Solution:**
```bash
pip install sendgrid python-dotenv
# Then restart Streamlit
```

### Issue 2: "Email not configured" in UI

**Symptoms:**
- Sidebar shows: "⚠️ Email not configured"
- Setup instructions shown

**Cause:** .env file missing or incorrect

**Solution:**
1. Check `.env` file exists in project root
2. Verify contents:
   ```bash
   SENDGRID_API_KEY=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
   SENDGRID_FROM_EMAIL=agovil@aurigincm.com
   SENDGRID_FROM_NAME=Aurigin Trade Processing
   ```
3. Restart Streamlit

### Issue 3: Email checkbox checked but no email sent

**Symptoms:**
- Checkbox is checked
- Recipients are entered
- Pipeline completes but no email received

**Diagnosis:**

Check the console/terminal for log messages:

**If you see:**
```
No email recipients specified - skipping email
```
**Solution:** Recipients not being passed correctly. Check session state.

**If you see:**
```
Email not sent - sendgrid package not installed
```
**Solution:** Install sendgrid: `pip install sendgrid python-dotenv`

**If you see:**
```
Email not sent - SendGrid not configured
```
**Solution:** Check .env file configuration

**If you see:**
```
Attempting to send email to: operations@aurigincm.com
Sending Stage 1 completion email...
❌ Failed to send completion email
```
**Solution:** Check SendGrid API key is valid and sender email is verified

### Issue 4: Email sent but not received

**Symptoms:**
- Console shows: "✅ Email sent successfully to..."
- But email not in inbox

**Diagnosis:**

1. **Check Spam/Junk folder**

2. **Check SendGrid Activity Log:**
   - Go to: https://app.sendgrid.com/email_activity
   - Look for recent sends
   - Check delivery status

3. **Verify recipient email is correct:**
   - Check for typos in email addresses
   - Verify operations@aurigincm.com is correct

4. **Check SendGrid sender verification:**
   - Sender (agovil@aurigincm.com) must be verified
   - Go to: https://app.sendgrid.com/settings/sender_auth

### Issue 5: API Key Error

**Symptoms:**
```
HTTP Error 401: Unauthorized
```

**Solution:**
1. Verify API key in `.env` is correct
2. Check API key hasn't been deleted in SendGrid
3. Verify API key has "Full Access" permissions
4. Try generating a new API key

### Issue 6: Recipients not showing in UI

**Symptoms:**
- Checkbox checked
- But no recipient count shown

**Solution:**
- Make sure you're entering valid email addresses
- Separate multiple emails with commas
- No extra spaces

## 📊 Debugging Steps

### Enable Detailed Logging

1. **Check Streamlit Console/Terminal:**
   - All log messages appear here
   - Look for email-related messages

2. **Check for these specific messages:**

   ✅ **Success messages:**
   ```
   Attempting to send email to: operations@aurigincm.com
   Sending Stage 1 completion email...
   ✅ Email sent successfully to operations@aurigincm.com
   ```

   ⚠️ **Warning messages:**
   ```
   Email not sent - sendgrid package not installed
   Email not sent - SendGrid not configured
   No email recipients specified - skipping email
   ```

   ❌ **Error messages:**
   ```
   ❌ Failed to send completion email
   ❌ Error sending completion email: [details]
   ```

### Test Email Manually

Create a test file `test_email.py`:

```python
from email_sender import EmailSender

sender = EmailSender()

if sender.is_enabled():
    print("Email is enabled!")

    success = sender.send_email(
        to_emails=['operations@aurigincm.com'],
        subject='Test Email',
        html_body='<h1>Test</h1><p>This is a test email.</p>'
    )

    if success:
        print("✅ Test email sent!")
    else:
        print("❌ Test email failed!")
else:
    print("❌ Email not enabled - check configuration")
```

Run it:
```bash
python test_email.py
```

## 🔍 Verification Checklist

Before running the pipeline, verify:

- [ ] `pip list | grep sendgrid` shows sendgrid installed
- [ ] `python email_sender.py` shows "Configured: True"
- [ ] `.env` file exists with correct values
- [ ] Streamlit sidebar shows "✓ Email configured"
- [ ] Checkbox "Send email on completion" is checked
- [ ] Recipient count shows at least 1
- [ ] Sender email (agovil@aurigincm.com) is verified in SendGrid

## 📧 SendGrid Dashboard Checks

1. **Verify Sender Authentication:**
   - https://app.sendgrid.com/settings/sender_auth
   - agovil@aurigincm.com should show "Verified"

2. **Check API Keys:**
   - https://app.sendgrid.com/settings/api_keys
   - Your API key should be listed
   - Should have "Full Access"

3. **Monitor Email Activity:**
   - https://app.sendgrid.com/email_activity
   - Shows all sent emails
   - Shows delivery status
   - Shows bounces/errors

4. **Check Usage:**
   - https://app.sendgrid.com/stats
   - Free tier: 100 emails/day
   - Monitor your usage

## 🆘 Still Not Working?

If email still doesn't work after all checks:

1. **Copy-paste console output** showing the error
2. **Check SendGrid Activity log** for delivery status
3. **Verify all environment variables** are set correctly
4. **Try sending a test email** using SendGrid web UI
5. **Check if sender email is actually verified** in SendGrid

## 📞 Support Resources

- SendGrid Docs: https://docs.sendgrid.com
- SendGrid API Reference: https://docs.sendgrid.com/api-reference
- SendGrid Support: https://support.sendgrid.com
- Check SendGrid Status: https://status.sendgrid.com
