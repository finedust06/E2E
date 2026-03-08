from Crypto.PublicKey import RSA

def generate_rsa_keypair():
    key = RSA.generate(2048)

    private_key = key.export_key()
    public_key = key.publickey().export_key()

    return private_key, public_key

def decrypt_data(private_key_pem, encrypted_text):
    private_key = RSA.import_key(private_key_pem)

    cipher = PKCS1_v1_5.new(private_key)

    encrypted_bytes = base64.b64decode(encrypted_text)

    decrypted = cipher.decrypt(encrypted_bytes, None)

    return decrypted.decode()