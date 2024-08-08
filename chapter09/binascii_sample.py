# バイナリデータを16進数やBase64などASCIIに変換する
# base64 や bytes.hex, bytes.fromhex などもある
import binascii

print(binascii.b2a_hex(b"hello"))
print(binascii.a2b_hex(b"68656c6c6f"))
print(binascii.b2a_base64(b"hello"))
print(binascii.a2b_base64(b"aGVsbG8="))
