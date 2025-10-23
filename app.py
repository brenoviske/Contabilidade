from flask import Flask , render_template , request , jsonify 
import os
from dotenv import load_dotenv
app = Flask(__name__)

# Loading .env file
load_dotenv()

# Gathering enviroment variables
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

@app.route('/', methods = ['GET','POST'])
def login():

    if request.method == 'POST':
        form  = request.form.to_dict()
        if form.get('username') == username and form.get('password') == password:
            return jsonify({
                'status': 'success',
            })
        return jsonify({
            'status':'error',
            'message':'Credenciais Inválidas'
        })
    return render_template('login.html')


# ===================
# Investiment Calculus
# ===================

@app.route('/investment_calc', methods = ['GET','POST'])
def investment():
    M = None # Just assuring that the variables exists just before the post route 
    if request.method == 'POST':
        form = request.form.to_dict()

        try:
            M = float( float(form.get('investmentAmount')) ) * ( (1 + float(form.get('rendiment'))/100) ** float(form.get('investmentDuration') ))
            return jsonify({
                'status':'success',
                'message': f'Valor esperado é de {M:.2f}'
            })
        
        except ( TypeError , ValueError):
            return jsonify({
                'status':'error',
                'message':'Valores inválidos'
            }) , 400
    return render_template('main.html')


# ==================
# Depreciation route
# ==================

@app.route('/depreciation_calc', methods = ['GET','POST'])
def deprec():

    valor_inicial , valor_resi , t ,dp = None
    if request.method == 'POST':
        form = request.form.to_dict()

        try:
            valor_inicial = float(form.get('initialValue'))
            valor_resi = float(form.get('residualPercentage')) / 100

            t = float(request.form.get('time'))

            dp = ( valor_inicial - (valor_inicial * valor_resi)) / t

            
            return jsonify({
                'status':'success',
                'message': f'Valor de depreciação(Linear Anual):{dp}'
            })
        
        except Exception as e:
            print('Error message:',e)
            return jsonify({
                'status':'error',
                'message':'Houve um erro durante o processamento'
            })
    return render_template('main.html')
                

# ==================
# Amortization route
# ==================

@app.route('/amortization_route', methods = ['GET','POST'])
def amortization():

    c , n , A = None

    if request.method == 'POST':
        form = request.form.to_dict()

        try:
            c = float( form.get('initialValue'))
            n = int( form.get('shares'))

            if n <= 0:
                return jsonify({
                    'status':'error',
                    'message':'Número de parcelas deve ser positivo e acima de zero'
                })
            
            if c < 0:
                return jsonify({
                    'status':'error',
                    'message':'Capital Incial deve ser positivo'
                })

            A = float( c / n) # Constant interest value of amortization

            return jsonify({
                'status':'success',
                'message':f'O valor constante amortizado é de : {A}'
            })
        except Exception as e :
            print('Error message:',e)
            return jsonify({
                'status':'error',
                'message':'Houve um erro durante o processamento'
            })
    return render_template('main.html')


#===========================
# Real State route
# ==========================

# ==================
# Real Estate route
# ==================
@app.route('/realstate_calc', methods=['POST', 'GET'])
def real_state():
    if request.method == 'POST':
        form = request.form.to_dict()
        try:
            initial_value = float(form.get('initialValue'))
            appreciation_rate = float(form.get('appreciationRate')) / 100  # convert % to decimal
            time = float(form.get('years'))

            final_value = initial_value * ((1 + appreciation_rate) ** time)
            appreciation_amount = final_value - initial_value
            appreciation_percent = (appreciation_amount / initial_value) * 100

            return jsonify({
                'status': 'success',
                'message': (
                    f'Valor futuro estimado: R$ {final_value:,.2f} '
                    f'(Valorização total: R$ {appreciation_amount:,.2f}, '
                    f'{appreciation_percent:.2f}%)'
                ).replace(',', 'X').replace('.', ',').replace('X', '.')
            })

        except Exception as e:
            print("Erro:", e)
            return jsonify({
                'status': 'error',
                'message': 'Valores inválidos ou campos incompletos.'
            }), 400

    return jsonify({
        'status': 'info',
        'message': 'Envie dados via POST para calcular a valorização.'
    })

# ================
# Main route 
# ================


@app.route('/main')
def main(): return render_template('main.html')


if __name__ == '__main__':
    app.run( debug = True)