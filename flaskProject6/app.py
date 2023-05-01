from random import randint

from flask import Flask, render_template, request, redirect, url_for
from logic import Authority
app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
userlist = []
authorities = []
colo = []
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Process form data here
        bit = request.form['bit']
        k = request.form['k']
        length = request.form['len']
        # Redirect to thank you page
        #Auth = Authority(bitlength=int(bit), k=int(k), t=int(length))
        Auth = Authority(bitlength=int(bit), k=int(k), t=int(length))
        # global auther
        # auther = Auth
        authorities.append(Auth)
        return redirect(url_for('home'))
    else:
        return render_template('form.html')

    # else:


@app.route('/thankyou/')
def thankyou():

    return render_template('user.html',thelist=userlist)

@app.route('/createuser/<id>', methods=['GET', 'POST'])
def createuser(id):
    # auther = authe
    ind = int(id)

    auther = authorities[ind-1]
    if request.method == 'POST':
        new_user = request.form['usertext']
        ischeat = request.form['is_cheat']
        # k = randint(0, 1)
        # print(k)
        # print(ischeat)
        if(ischeat=="True"):
            # print('s')
            newer = auther.create_user(I=new_user, cheat=True)
        else:
            # print('t')
            newer = auther.create_user(I=new_user)
            # print("ss")

        userlist.append(newer)

        # for i in userlist:
        # print(auther.verify(newer))
        check=1
        for j in range(1000):
            if(auther.verify(newer)==False):
                # print("sst")
                colo.append(0)
                check=0
                break

        if(check==1):
            colo.append(1)

        return render_template('user.html',thelist=userlist,id=id,colo=colo)
    else:
       return render_template('createuser.html',id=id)

@app.route('/chosea', methods=['GET'])
def chosea():
    # # auther = authe
    # ind = int(id)
    # auther = authorities[ind]
    # if request.method == 'POST':
    #     new_user = request.form['usertext']
    #     newer = auther.create_user(I=new_user)
    #     userlist.append(newer)
    #     return render_template('user.html',thelist=userlist)
    # else:
       return render_template('choseauth.html',items=authorities)

@app.route('/choseauth/<id>', methods=['GET','POST'])
def choseauth(id):
    # auther = authe
    ind = int(id)
    auther = authorities[ind-1]
    if request.method == 'POST':
        new_user = request.form['usertext']
        newer = auther.create_user(I=new_user)
        userlist.append(newer)
        return render_template('user.html',thelist=userlist)
    else:
       return redirect(url_for('createuser',id=id))



if __name__ == '__main__':
    app.run(debug=True)