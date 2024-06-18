def vigenere_encrypt(text_for_encrypt, keyword):
    text_for_encrypt = text_for_encrypt.upper()
    keyword = keyword.upper()

    extended_keyword = (keyword * (len(text_for_encrypt) // len(keyword) + 1))[:len(text_for_encrypt)]

    ciphertext = ''

    for i in range(len(text_for_encrypt)):
        p_char = text_for_encrypt[i]
        k_char = extended_keyword[i]
        if p_char.isalpha():
            c_char = chr(((ord(p_char) - ord('A') + ord(k_char) - ord('A')) % 26) + ord('A'))
        ciphertext += c_char

    return ciphertext


# Пример использования функции для шифрования
text_for_encrypt = input("Введите слово для шифрования: ")
keyword = input("Ввдеите ключ для шифрования: ")
encrypted_message = vigenere_encrypt(text_for_encrypt, keyword)
print(f"Зашифрованное сообщение: {encrypted_message}")
