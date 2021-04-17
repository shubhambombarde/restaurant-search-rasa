# rasa-chatbot-upgrad-assignment
Repo for collaborating on the Rasa Chatbot Assignment

# Steps to run the project
- rasa run actions: Opens actions.py as a server 
- rasa shell: Initializes chatbot in shell

# Other commands
- rasa train: Trains NLU and core

# Mail Integration
- All the mails associated with this project are sent using SendGrid Mail API.
- We went with SendGrid because using Google SMTP server would expose the credentials for the account.
- Since we are using the free quota from SendGrid, we only have a quota of 100 mails / day
- Please check Spam Box for recieved mails. 
- If mails couldn't be delivered, it is possibly due to issue with SendGrid API key which may be expired (free quota).
