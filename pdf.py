from flask import Flask, jsonify, request, send_file, render_template_string
from PyPDF2 import PdfWriter, PdfReader
import os
import tempfile

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        # Process the file
        reader = PdfReader(file.stream)
        writer = PdfWriter()

        page = reader.pages[-1]
        page.rotate(90)
        page.cropbox.lower_left = (29, 179)
        page.cropbox.upper_right = (504, 496)
        writer.add_page(page)

        # Save the processed file to a temporary file
        temp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        writer.write(temp)
        temp.close()

        # Return the URL to the file
        return jsonify({'url': f'/download/{os.path.basename(temp.name)}'})

@app.route('/download/<filename>')
def download_file(filename):
    temp_path = os.path.join(tempfile.gettempdir(), filename)
    return send_file(temp_path, as_attachment=False)

@app.route('/')
def index():
    return render_template_string('''
    <!doctype html>
    <html>
    <head>
    <title>Upload StockX PDF</title>
    <style>
    /* Your CSS Starts Here */
    body {
      font-family: sans-serif;
      background-color: #eeeeee;
    }

    .file-upload {
      background-color: #ffffff;
      width: 600px;
      margin: 0 auto;
      padding: 20px;
    }

    .file-upload-btn {
      width: 100%;
      margin: 0;
      color: #fff;
      background: #1FB264;
      border: none;
      padding: 10px;
      border-radius: 4px;
      border-bottom: 4px solid #15824B;
      transition: all .2s ease;
      outline: none;
      text-transform: uppercase;
      font-weight: 700;
    }

    .file-upload-btn:hover {
      background: #1AA059;
      color: #ffffff;
      transition: all .2s ease;
      cursor: pointer;
    }

    .file-upload-btn:active {
      border: 0;
      transition: all .2s ease;
    }

    .file-upload-content {
      display: none;
      text-align: center;
    }

    .file-upload-input {
      position: absolute;
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      outline: none;
      opacity: 0;
      cursor: pointer;
    }

    .image-upload-wrap {
      margin-top: 20px;
      border: 4px dashed #1FB264;
      position: relative;
    }

    .image-dropping,
    .image-upload-wrap:hover {
      background-color: #1FB264;
      border: 4px dashed #ffffff;
    }

    .image-title-wrap {
      padding: 0 15px 15px 15px;
      color: #222;
    }

    .drag-text {
      text-align: center;
    }

    .drag-text h3 {
      font-weight: 100;
      text-transform: uppercase;
      color: #15824B;
      padding: 60px 0;
    }

    .file-upload-image {
      max-height: 200px;
      max-width: 200px;
      margin: auto;
      padding: 20px;
    }

    .remove-image {
      width: 200px;
      margin: 0;
      color: #fff;
      background: #cd4535;
      border: none;
      padding: 10px;
      border-radius: 4px;
      border-bottom: 4px solid #b02818;
      transition: all .2s ease;
      outline: none;
      text-transform: uppercase;
      font-weight: 700;
    }

    .remove-image:hover {
      background: #c13b2a;
      color: #ffffff;
      transition: all .2s ease;
      cursor: pointer;
    }

    .remove-image:active {
      border: 0;
      transition: all .2s ease;
    }
    /* Your CSS Ends Here */
    </style>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
    </head>
    <body>
    <!-- Your HTML Starts Here -->
    <script class="jsbin" src="https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
    <div class="file-upload">
      <button class="file-upload-btn" type="button" onclick="$('.file-upload-input').trigger( 'click' )">Add StockX PDF</button>
      <div class="image-upload-wrap">
        <input class="file-upload-input" type='file' onchange="readURL(this);" accept="application/pdf" />
        <div class="drag-text">
          <h3>Drag and drop a StockX PDF or select add StockX PDF</h3>
        </div>
      </div>
    </div>
    <!-- Your HTML Ends Here -->
    <script>
    /* Your JavaScript Starts Here */
    function readURL(input) {
      if (input.files && input.files[0]) {

        var reader = new FileReader();

        reader.onload = function(e) {
          // Upload the file after selection
          var formData = new FormData();
          formData.append('file', input.files[0]);

          $.ajax({
              url: '/upload',
              type: 'POST',
              data: formData,
              processData: false,
              contentType: false,
              success: function(data) {
                  if (data.url) {
                      window.open(data.url, '_blank');
                  }
              },
              error: function(xhr, status, error) {
                  console.error('Upload error:', error);
              },
              complete: function() {
                // Reset the file input after upload
                $('.file-upload-input').val('');
            }
          });
        };

        reader.readAsDataURL(input.files[0]);

      } else {
        removeUpload();
      }
    }

    
    /* Your JavaScript Ends Here */
    </script>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
