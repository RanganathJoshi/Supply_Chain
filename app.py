from src.SupplyChainPricing.Pipeline.Prediction import CustomData,PredictPipeline
from flask import Flask,request,render_template


app=Flask(__name__)

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route("/predict",methods=['GET','POST'])
def predict_datapoint():
    if request.method=="GET":
        return render_template('form.html')
    else:
        po_so_=request.form.get('po_/_so_#')
        asn_dn =request.form.get('asn/dn_#')
        country=float(request.form.get('country'))
        fulfill_via=request.form.get('fulfill_via')
        vendor_inco_term=request.form.get('vendor_inco_term')
        shipment_mode=request.form.get('shipment_mode')
        sub_classification=request.form.get('sub_classification')
        vendor=request.form.get('vendor')
        brand=request.form.get('brand')
        unit_of_measure=float(request.form.get('unit_of_measure'))
        line_item_quality=float(request.form.get('line_item_quality'))
        pack_price=float(request.form.get('pack_price'))
        unit_price=float(request.form.get('unit_price'))
        line_item_value=float(request.form.get('line_item_value'))
        manufacturing_site=request.form.get('manufacturing_site')
        first_line_designation=request.form.get('first_line_designation')
        freight_cost_=float(request.form.get('freight_cost_'))
        line_item_insurance_=float(request.form.get('line_item_insurance_'))
        days_to_process=float(request.form.get('days_to_process'))



    custom_data=CustomData()
    data=custom_data.get_data_as_dataframe([po_so_,asn_dn,country,fulfill_via,vendor_inco_term,shipment_mode,
                                            sub_classification,vendor,brand,unit_of_measure,line_item_quality,pack_price,unit_price,
                                            line_item_value,manufacturing_site,first_line_designation,freight_cost_,line_item_insurance_,
                                            days_to_process])
    predict=PredictPipeline()
    pred=predict.predict(data)
    
    return render_template('result.html',final_result=pred)




if __name__=='__main__':
    app.run(host="0.0.0.0",port=5000)
    



