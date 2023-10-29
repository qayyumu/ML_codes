from app import server

if __name__ == "__main__":
    # server.run(debug=False)
    server.run(debug = False, port = 8000, host = '0.0.0.0', threaded = True)
    # server.run(host='0.0.0.0', port=8000)


# if __name__ == '__main__':
#     server.run(debug=False,port=5000)
#     # server.run(ssl_context=("njcertificate.crt", "nj-decrypted.key"),debug=False)
    
#     # app.run(host="148.66.135.64",port=120)
#     # app.run(host="0.0.0.0",port=5000)
#     #  app.run(host="127.0.0.1", port=801, threaded=True)

