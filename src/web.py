from flask import Flask, render_template
app = Flask(__name__)

@app.route("/snapshot")
def get_snapshot():
	return 'hi'

app.run(port=8080)
