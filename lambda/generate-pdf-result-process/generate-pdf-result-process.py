from xhtml2pdf import pisa  

def handler():
    source_html = """<!DOCTYPE html>
    <html>

    <head>

    <style>  

    body {
    font-family: 'Arial';
    padding: 2cm;  
    background: none;  
    }

    .container {
    width: auto;
    background: white; 
    border: 15px solid #eee;
    padding: 3cm 2cm;
    }

    h1 {
    font-size: 28px;
    text-transform: uppercase;    
    border-bottom: 1px solid black;
    letter-spacing: 5px;   
    }  

    .form-row {     
    margin-bottom: 1cm;    
    }

    label {
    font-size: 14px;
    text-transform: uppercase;
    display: block;
    letter-spacing: 1px; 
    }

    input[type="text"] {
    width: 100%;      
    margin-top: 5px; 
    border-bottom: 1px solid black;  
    }

    textarea {
    width: 100%;
    height: 5cm;  
    border: 1px solid #bbb;   
    }

    </style>  

    </head>

    <body>  

    <div class="container">

    <h1>Resultado de la verificación</h1>  

    <div class="form-row">    

    <label>Fecha de la verificación</label>  
    <input type="text">

    </div>  

    <div class="form-row">
    
    <label>Nombre de la entidad</label>
    <input type="text">  

    </div>  

    <div class="form-row">
        
    <label>NIT</label>
    <input type="text">
    
    </div>

    <div class="form-row">
    
    <label>Usuario</label>  
    <input type="text">  

    </div> 

    <div class="form-row">

    <label>Nombre del cliente</label>
    <input type="text">  

    </div>

    <div class="form-row">
    
    <label>Número de documento</label>
    <input type="text">   

    </div> 

    <div class="form-row">
    
    <label>ID Petición</label>
    <input type="text">

    </div>

    <div class="form-row">

    <label>Observaciones</label>
    <textarea></textarea>  
    
    </div>

    </div>  

    </body>
    </html> """

    lambda_client = boto3.client("lambda")
    event = {
        'queryStringParameters': {
            'id': '434243'
        }
    }

    event_json = json.dumps(event)
    invoke_params = {
        'FunctionName':'',
        'InvocationType':'RequestResponse',
        'Payload':event_json,
    }

    response = lambda_client.invoke(**invoke_params)
    result = response['Payload'].read()
    print("THISSSSSSS",result)
