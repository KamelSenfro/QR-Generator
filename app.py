import io
import qrcode
from flask import Flask, request, send_file, make_response

app = Flask(__name__)

# function to generate a QR code from a URL
def generate_qr_code(url):
    # create a QR code object with a version of 1, a box size of 10, and a border of 5
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    # add the URL to the QR code object
    qr.add_data(url)
    # make the QR code fit the data
    qr.make(fit=True)
    # create an image from the QR code with a black fill color and white background color
    img = qr.make_image(fill_color="black", back_color="white")
    # create a byte array to store the image data
    img_byte_array = io.BytesIO()
    # save the image data to the byte array in PNG format
    img.save(img_byte_array, format='PNG')
    # return the byte array value
    return img_byte_array.getvalue()

# route to generate a QR code from a URL
@app.route('/generate_qr_code', methods=['GET'])
def qr_code_api():
    # get the URL parameter from the request
    url = request.args.get('url', '')
    if url:
        try:
            # generate the QR code image data
            qr_image_data = generate_qr_code(url)
            # create a response with the image data as an attachment
            response = make_response(send_file(io.BytesIO(qr_image_data), mimetype='image/png'))
            response.headers.set('Content-Disposition', 'attachment', filename='qr_code.png')
            return response
        except Exception as e:
            # return an error message if there was an error generating the QR code
            return f"Error generating QR code: {str(e)}", 500
    else:
        # return an error message if no URL parameter was provided
        return "Invalid URL provided.", 400

# run the Flask app on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)