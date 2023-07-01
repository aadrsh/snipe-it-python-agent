# snipe-it-python-agent
Python script that can be used as snipe-it asset scanning agent

Hi,
Steps to use this agent
1. Modify it according to your needs (I have already created fieldsets in snipe-it that are being used here)
2. Add your API Key and Snipe IT Url
3. Convert this to exe using "pyinstaller --onefile agent.py"
4. Create a GPO in Active Directory and configure a task scheduler that runs "on idle" trigger for your need of time
5. Host the generated exe in smb share in local network and add its location in "action trigger"
6. dont forget to run the scheduler as SYSTEM user
