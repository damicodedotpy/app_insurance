# ******************************PYTHON LIBRARIES******************************
from io import BytesIO
import os
# ******************************EXTERNAL LIBRARIES****************************
from flask import Flask, request, send_file, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from pandas import DataFrame, ExcelWriter
import xlsxwriter
import openpyxl
# ******************************OWN LIBRARIES*********************************
from extensions import db
from src.models.Unit import UnitModel
from src.models.Business import BusinessModel
from src.models.Insurance import InsuranceModel
from schemas import BasicUnitSchema, BasicBusinessSchema, BasicInsuranceSchema
# ****************************************************************************

blp = Blueprint("excel", __name__, description="All export functionalities")

@blp.route("/export/")
class ExportExcelView(MethodView):
    def get(self):
        
        database_requested = request.args.get("database")
        if database_requested == "units":
            
            try:
                database = UnitModel.query.all()
            except:
                return jsonify({"message": "Something has occurred while getting the database"})
            
            try:
                schema_units = BasicUnitSchema(many=True)
                units_data = schema_units.dump(database)
            except:
                return jsonify({"message": "Something has occurred while serializing the database."})
            
            try:
                df_units = DataFrame(units_data)
            except:
                return jsonify({"message": "Something has occurred while creating the DataFrame."})
            
            try:
                output = BytesIO() #BytesIO es un metodo que crea un espacio de almacenamiento en la memoria RAM para informacion de tipo binaria, su ventaja de que se guarde dentro de este espacio de memoria es que aquello que haya sido guardado ahi puede ser tratado como un archivo guardado en el disco local pero sin ocupar memoria de disco duro o servidor.
                writer = ExcelWriter(output, engine="xlsxwriter") # ExcelWriter de pandas se utiliza para escribir los datos del DataFrame en el archivo de Excel.
                df_units.to_excel(writer)
                writer.save()
                output.seek(0) # Cuando escribimos en un objeto BytesIO() el puntero avanza a medida que se escriben nuevos bytes dentro de el. Con el metodo seek() nos aseguramos de que reposicionar el puntero al principio de la infomracion binaria para que el documento que se envia al mentodo send_file() llegue completo y no con solo un fragmento del binario provocando errores.               
            except Exception as e:
                return jsonify({"message": f"Something has occurred while creating the excel file. {e}"})
                
                
                
        elif database_requested == "business":
            try:
                database = BusinessModel.query.all()
            except Exception as e:
                return jsonify({"message": f"Something has occurred while getting the database. {e}"})
            
            try:
                schema_business = BasicBusinessSchema(many=True)
                business_data = schema_business.dump(database)
            except Exception as e:
                return jsonify({"message": f"Something has occurred while serializing the database. {e}"})
            
            try:
                df_business = DataFrame(business_data)
            except Exception as e:
                return jsonify({"message": f"Something has occurred while creating the DataFrame. {e}"})
            
            try:
                output = BytesIO()
                writer = ExcelWriter(output, engine="xlsxwriter") 
                df_business.to_excel(writer)
                writer.save()
                output.seek(0)
            except Exception as e:
                return jsonify({"message": f"Something has occurred while creating the excel file. {e}"})
            
            
        elif database_requested == "insurance":
            try:
                database = InsuranceModel.query.all()
            except Exception as e:
                return jsonify({"message": f"Something has occurred while getting the database. {e}"})
            
            try:
                schema_insurance = BasicInsuranceSchema(many=True)
                insurance_data = schema_insurance.dump(database)
            except Exception as e:
                return jsonify({"message": f"Something has occurred while serializing the database. {e}"})
            
            try:
                df_insurance = DataFrame(insurance_data)
            except Exception as e:
                return jsonify({"message": f"Something has occurred while creating the DataFrame. {e}"})
            
            try:
                output = BytesIO()
                writer = ExcelWriter(output, engine="xlsxwriter") 
                df_insurance.to_excel(writer)
                writer.save()
                output.seek(0)
            except Exception as e:
                return jsonify({"message": f"Something has occurred while creating the excel file. {e}"})
        
        return send_file(output, 
                         as_attachment=True, 
                         mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                         download_name=f"{database_requested}_database.xlsx"
                         )
    
        
        
