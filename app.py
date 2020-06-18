import os
import sys
module_path = os.path.abspath(os.getcwd() + '\\..')
if module_path not in sys.path:
    sys.path.append(module_path)



import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
import cloudpickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
custom_pipeline = cloudpickle.load(open('custom_pipeline_cloudpickle.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')



@app.route('/predict',methods=['POST'])
def predict():

	#taking in the user input
	job_fields = [x for x in request.form.values()]
	input_df = pd.DataFrame({'company_profile': job_fields[0], 
	'description': job_fields[1],'requirements': job_fields[2],'benefits': job_fields[3], 'has_company_logo': int(job_fields[4]),
	'telecommuting': int(job_fields[5]), 'has_questions': int(job_fields[6])}, index=[0])
	test_vector = custom_pipeline(input_df)    
	prediction = model.predict_proba(test_vector)
	
	if prediction[0][0] > prediction[0][1]:
		op_string = str(int(prediction[0][0]*100)) + '% real'
	else:
		op_string = str(int(prediction[0][1]*100)) + '% fake'
	
	output = 100
	return render_template('index.html', prediction_text='This job posting is '+op_string)


# @app.route('/results',methods=['POST'])
# def results():
#
#     data = request.get_json(force=True)
#     prediction = model.predict([np.array(list(data.values()))])
#
#     output = prediction[0]
#     return jsonify(output)


if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)