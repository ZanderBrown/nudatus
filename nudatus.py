import token
import tokenize
from io import BytesIO, StringIO

def mangle(text):
    """
    Takes a script and mangles it to fit inside 8192 bytes if necessary
    """

    text_bytes = text.encode('utf-8')

    # Wrap the input script as a byte stream
    buff = BytesIO(text_bytes)
    # String stream for the mangled script
    mangled = StringIO()

    last_tok = token.INDENT
    last_line = -1
    last_col = 0
    last_line_text = ''

    # Build tokens from the script
    tokens = tokenize.tokenize(buff.readline)
    for t, text, (line_s, col_s), (line_e, col_e), line in tokens:
        # If this is a new line (except the very first)
        if line_s > last_line and last_line != -1:
            # Reset the column
            last_col = 0
            # If the last line ended in a '\' (continuation)
            if last_line_text.rstrip()[-1:] == '\\':
                # Recreate it
                mangled.write(' \\\n')

        # If this is a docstring comment
        if t == token.STRING and (last_tok == token.INDENT or
            last_tok == token.NEWLINE or last_tok == tokenize.NL):
            # Output number of lines corresponding those in
            # the docstring comment
            mangled.write('\n' * (len(text.split('\n')) - 1))
        # Or is it a standard comment
        elif t == tokenize.COMMENT:
            # Plain comment, just don't write it
            pass
        else:
            # Recreate indentation, ideally we should use tabs
            if col_s > last_col:
                mangled.write(" " * (col_s - last_col))
            # This is a bit odd by without it the script seems
            # to be prefixed with utf-8, making it invalid
            if text != 'utf-8' and last_line != -1:
                mangled.write(text)

        last_tok = t
        last_col = col_e
        last_line = line_e
        last_line_text = line

    # The flashing system expects bytes
    result = mangled.getvalue()
    saved = len(text_bytes) - len(result)
    percent = saved / len(text_bytes) * 100
    return (result, saved, percent)

with open('nudatus.py', 'r') as f:
    result, saved, percent = mangle(f.read())
    print(result)
