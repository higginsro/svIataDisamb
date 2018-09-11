from flask import Flask, jsonify, request,Blueprint
from findCandidates import run as disambiguate
import os,re
from logger.customLogger import CustomLogger

app = Flask(__name__)
service = Blueprint("Three letter swedish word disambiguation service", __name__)
base_dir = os.path.dirname(os.path.abspath(__file__)) 
conf_file = os.path.join(base_dir, "conf", "logging.ini")
logger = CustomLogger(conf_file)

@service.route("/v0/api/disambiguate", methods = ["GET"])
def run_disambiguation():
	try:
    		phrase = request.args["message"]
    		phrase = re.sub(r"\s+"," ", phrase).lower()
    		result = disambiguate(phrase)
		logger.log("INFO", "Swedish Three Letter Disambiguation", "Controller", "run_disambiguation", "input message : {}, output: {}".format(phrase.encode("utf-8"), result))
   		return jsonify(result = result, status = 200)
	except Exception as err:
		print err.message, err.args
		# logger.log("ERROR","Swedish  3l disamb","Controller", "run_disambiguation", err)
		return jsonify(result = {"probably_airports" : [], "probably_not_airports" : []}, status = 500)
	

app.register_blueprint(service, url_prefix = "/sviatadisambiguation")

if __name__ == "__main__":
	app.run("localhost",5000)
