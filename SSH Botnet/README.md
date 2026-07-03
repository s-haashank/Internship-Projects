# SSH Botnet Controller

This project is an educational tool for understanding how botnets can be managed via SSH. It demonstrates how to:
- Add clients (bots) via SSH.
- Send remote commands to multiple systems.
- Manage sessions and automate actions.

##  Project Structure
- `botnet.py` - Main script to run the botnet controller
- `hosts.txt` - List of target SSH-enabled IPs
- `wordlist.txt` - Passwords used to connect to SSH hosts
- `logs/` - Folder to store command execution logs

## ⚙️ How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
