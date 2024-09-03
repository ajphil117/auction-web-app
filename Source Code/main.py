from auction import create_app

# Initiate app
if __name__=='__main__':
    napp=create_app()
    napp.run(debug=True)