import hashlib

h = hashlib.new("sha256")
h.update(b"Hello, ")
h.update(b"World!")
print(h.digest())
print(h.hexdigest())
print(h.digest_size)
