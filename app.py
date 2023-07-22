import io
import qrcode
from flask import Flask, request, send_file, make_response

app = Flask(__name__)

def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='PNG')
    return img_byte_array.getvalue()

@app.route('/generate_qr_code', methods=['GET'])
def qr_code_api():
    url = request.args.get('url', '')
    if url:
        try:
            qr_image_data = generate_qr_code(url)
            response = make_response(send_file(io.BytesIO(qr_image_data), mimetype='image/png'))
            response.headers.set('Content-Disposition', 'attachment', filename='qr_code.png')
            return response
        except Exception as e:
            return f"Error generating QR code: {str(e)}", 500
    else:
        return "Invalid URL provided.", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
