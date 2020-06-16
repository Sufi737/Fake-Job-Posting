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
    input_df = pd.DataFrame({'company_profile': job_fields[0], 'description': job_fields[1],'requirements': job_fields[2],'benefits': job_fields[3]})
    # prediction = model.predict(final_features)

    # output = round(prediction[0], 2)
    output = 100
    return render_template('index.html', prediction_text='Sales should be $ {}'.format(job_fields[0]))


# @app.route('/results',methods=['POST'])
# def results():
#
#     data = request.get_json(force=True)
#     prediction = model.predict([np.array(list(data.values()))])
#
#     output = prediction[0]
#     return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)