import tempfile

with tempfile.TemporaryFile() as tmp_file:

    tmp_file.write(b'192.168.0.1')
    tmp_file.seek(0)
    print(tmp_file.read().decode('utf-8'))