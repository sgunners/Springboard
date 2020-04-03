from flask import Flask, render_template, request, Markup

import predictions
import pandas as pd
import base64
import matplotlib.pyplot as plt

plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True

app= Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
@app.route("/index.html", methods=['POST', 'GET'])
def index():
    #blank defaults so it runs on startup
    main_text1 = 'In the box below, input your Twitter username (without the @ symbol), and the model will predict on your 200 most recent tweets. '
    main_text2 = 'Note: The process will take a moment and will refresh the page. Make sure to scroll for results'
    text_scroll=''
    text_in = ''
    text_out = ''
    df = pd.DataFrame()
    chart = ''
    bar = ''
    error_text=''
    results = ""
    in_text = ""
    word_title = ''
    word_text = ''
    prob_text = ''
    fic_nonfic_text = ''
    best_tweet_form=''
    url_string = ''
    tweet_test = '<blockquote class="twitter-tweet" data-conversation="none"><p lang="en" dir="ltr"><a href="https://twitter.com/jimmyfallon/status/1245871404110606337"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
    if request.method == 'POST':
            text_scroll='Scroll for Results!'
            text_in = request.form['text_in']
            value, df, wordcloud, best_value, final_best = predictions.final_tweet_model(text_in)
            url_string = "https://twitter.com/{}/status/{}".format(text_in,final_best[1][0])
            best_tweet_form = '<blockquote class="twitter-tweet" data-conversation="none"><p lang="en" dir="ltr"><a href="{}"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'.format(url_string)
            fic_nonfic_text = "The probility of your tweets being non-fiction is {:.2%} and the probability of your tweets being fiction is {:.2%}".format(value,1-value)
            results = 'Results'
            in_text = "Input text: "
            main_text1 = 'Try another username'
            main_text2 = ''
            if value<0.5:
        	    text_out = "This is Fiction"
        	    prob_text = 'Graph of Probability of Genres'
        	    df = df.sort_values('Probability')
        	    fig_bar = plt.figure()
        	    ax_bar = plt.subplot(111)
        	    ax_bar.barh(df.index, df['Probability']*100)
        	    fig_bar.savefig('/home/sgunners/main/hbar.png', bbox_inches='tight')
        	    with open("/home/sgunners/main/hbar.png","rb") as img_file:
        	        my_string2 = base64.b64encode(img_file.read()).decode()
        	    bar = Markup('<img src="data:image/png;base64,{}" width: 600px; height: 400px>'.format(my_string2))
        	    wordcloud.to_file("/home/sgunners/main/wc.png")
        	    with open("/home/sgunners/main/wc.png","rb") as img_file:
        	        my_string = base64.b64encode(img_file.read()).decode()
        	    chart = Markup('<img src="data:image/png;base64,{}" width: 600px; height: 400px>'.format(my_string))
        	    word_title = "Word Cloud"
        	    word_text = "Below is a wordcloud of the words that indicated the most probable genre of the input, with larger worde having a larger effect on the model."
        	    df = df.sort_values('Probability', ascending=False)
            else:
        	    text_out = "This is Non-Fiction"
    return render_template("index.html",
                            text_scroll=text_scroll,
                            text_in=text_in,
                            text_out=text_out,
                            tables=[df.to_html(classes='data', header="true")],
                            title='Results',
                            chart = chart,
                            error_text=error_text,
                            results = results,
                            in_text = in_text,
                            word_title = word_title,
                            word_text = word_text,
                            bar=bar,
                            prob_text=prob_text,
                            main_text1=main_text1,
                            main_text2=main_text2,
                            fic_nonfic_text=fic_nonfic_text,
                            tweet_test=tweet_test,
                            best_tweet_form = best_tweet_form,
                            url_string = url_string)

@app.route("/summ.html", methods=['POST','GET'])
def summ():
   #blank defaults so it runs on startup
    text_scroll=''
    text_in = ''
    text_out = ''
    df = pd.DataFrame()
    prob_text = ''
    bar=''
    chart = ''
    error_text=''
    results = ""
    in_text = ""
    word_title = ''
    word_text = ''
    fic_nonfic_text=''
    if request.method == 'POST':
            text_scroll='Scroll for Results!'
            text_in = request.form['text_in']
            value, df, wordcloud= predictions.final_text_model(text_in)
            fic_nonfic_text = "The probility of your text being non-fiction is {:.2%} and the probability of your text being fiction is {:.2%}".format(value,1-value)
            results = 'Results'
            in_text = "Input text: "
            if value<0.5:
        	    text_out = "This is Fiction"
        	    prob_text = 'Graph of Probability of Genres'
        	    df = df.sort_values('Probability')
        	    fig_bar = plt.figure()
        	    ax_bar = plt.subplot(111)
        	    ax_bar.barh(df.index, df['Probability'])
        	    fig_bar.savefig('/home/sgunners/main/hbar.png', bbox_inches='tight')
        	    with open("/home/sgunners/main/hbar.png","rb") as img_file:
        	        my_string2 = base64.b64encode(img_file.read()).decode()
        	    bar = Markup('<img src="data:image/png;base64,{}" width: 600px; height: 400px>'.format(my_string2))
        	    wordcloud.to_file("/home/sgunners/main/wc_summ.png")
        	    with open("/home/sgunners/main/wc_summ.png","rb") as img_file:
        	        my_string = base64.b64encode(img_file.read()).decode()
        	    chart = Markup('<img src="data:image/png;base64,{}" width: 600px; height: 400px>'.format(my_string))
        	    word_title = "Word Cloud"
        	    word_text = "Below is a wordcloud of the words that indicated the most probable genre of the input, with larger worde having a larger effect on the model."
        	    df = df.sort_values('Probability', ascending=False)
            else:
        	    text_out = "This is Non-Fiction"
    return render_template("summ.html",
                            text_scroll=text_scroll,
                            text_in=text_in,
                            text_out=text_out,
                            tables=[df.to_html(classes='data', header="true")],
                            title='Results',
                            chart = chart,
                            error_text=error_text,
                            results = results,
                            in_text = in_text,
                            word_title = word_title,
                            word_text = word_text,
                            bar=bar,
                            prob_text=prob_text,
                            fic_nonfic_text=fic_nonfic_text)

@app.route("/project_write.html")
def project_write():
    return render_template("project_write.html")

@app.route("/barack_obama.html")
def bo():
    value, df, wordcloud, best_value, final_best = predictions.final_tweet_model('BarackObama')
    text_in = "BarackObama"
    url_string = "https://twitter.com/{}/status/{}".format(text_in,final_best[1][0])
    fic_nonfic_text = "The probility of Barack Obama's Twitter being non-fiction is {:.2%} and the probability of it being fiction is {:.2%}".format(value,1-value)
    best_tweet_form = '<blockquote class="twitter-tweet" data-conversation="none"><p lang="en" dir="ltr"><a href="{}"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'.format(url_string)
    results = 'Results'
    in_text = 'Input text: '
    text_out = "This is Non-Fiction"
    text_scroll = "Scroll for Results"
    return render_template("barack_obama.html",text_in = text_in, text_scroll=text_scroll, results=results,in_text=in_text, text_out=text_out, url_string=url_string,best_tweet_form=best_tweet_form, fic_nonfic_text=fic_nonfic_text)

@app.route("/goodcaptain.html")
def good():
    value, df, wordcloud, best_value, final_best = predictions.final_tweet_model('goodcaptain')
    results = 'Results'
    fic_nonfic_text = "The probability of The Good Captain's tweets being non-fiction is {:.2%} and the probability of it being fiction is {:.2%}".format(value,1-value)
    url_string = "https://twitter.com/{}/status/{}".format('goodcaptain',final_best[1][0])
    best_tweet_form = '<blockquote class="twitter-tweet" data-conversation="none"><p lang="en" dir="ltr"><a href="{}"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'.format(url_string)
    text_out = "This is Fiction"
    df = df.sort_values('Probability')
    fig_bar = plt.figure()
    ax_bar = plt.subplot(111)
    ax_bar.barh(df.index, df['Probability'])
    fig_bar.savefig('/home/sgunners/main/hbar_gc.png', bbox_inches='tight')
    with open("/home/sgunners/main/hbar_gc.png","rb") as img_file:
        my_string_gc = base64.b64encode(img_file.read()).decode()
    bar = Markup('<img src="data:image/png;base64,{}" width: 600px; height: 400px>'.format(my_string_gc))
    wordcloud.to_file("/home/sgunners/main/wc_gc.png")
    with open("/home/sgunners/main/wc_gc.png","rb") as img_file:
    	my_string = base64.b64encode(img_file.read()).decode()
    chart = Markup('<img src="data:image/png;base64,{}" width: 600px; height: 400px>'.format(my_string))
    word_title = "Word Cloud"
    word_text = "Below is a wordcloud of the words that indicated the most probable genre of the input, with larger worde having a larger effect on the model."
    df = df.sort_values('Probability', ascending=False)
    return render_template("goodcaptain.html",
                            text_out=text_out,
                            tables=[df.to_html(classes='data', header="true")],
                            title='Results',
                            chart = chart,
                            results = results,
                            word_title = word_title,
                            word_text = word_text,
                            bar=bar,
                            fic_nonfic_text = fic_nonfic_text,
                            best_tweet_form=best_tweet_form)

@app.route("/mayoremanuel.html")
def mayor():
    value, df, wordcloud, best_value, final_best = predictions.final_tweet_model('mayoremanuel')
    results = 'Results'
    fic_nonfic_text = "The probability of Mayor Emanuel's tweets being non-fiction is {:.2%} and the probability of it being fiction is {:.2%}".format(value,1-value)
    url_string = "https://twitter.com/{}/status/{}".format('mayoremanuel',final_best[1][0])
    best_tweet_form = '<blockquote class="twitter-tweet" data-conversation="none"><p lang="en" dir="ltr"><a href="{}"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'.format(url_string)
    text_out = "This is Fiction"
    df = df.sort_values('Probability')
    fig_bar = plt.figure()
    ax_bar = plt.subplot(111)
    ax_bar.barh(df.index, df['Probability'])
    fig_bar.savefig('/home/sgunners/main/hbar_me.png', bbox_inches='tight')
    with open("/home/sgunners/main/hbar_me.png","rb") as img_file:
        my_string_me = base64.b64encode(img_file.read()).decode()
    bar = Markup('<img src="data:image/png;base64,{}" width: 600px; height: 400px>'.format(my_string_me))
    wordcloud.to_file("/home/sgunners/main/wc_me.png")
    with open("/home/sgunners/main/wc_me.png","rb") as img_file:
    	my_string = base64.b64encode(img_file.read()).decode()
    chart = Markup('<img src="data:image/png;base64,{}" width: 600px; height: 400px>'.format(my_string))
    word_title = "Word Cloud"
    word_text = "Below is a wordcloud of the words that indicated the most probable genre of the input, with larger worde having a larger effect on the model."
    df = df.sort_values('Probability', ascending=False)
    return render_template("mayoremanuel.html",
                            text_out=text_out,
                            tables=[df.to_html(classes='data', header="true")],
                            title='Results',
                            chart = chart,
                            results = results,
                            word_title = word_title,
                            word_text = word_text,
                            bar=bar,
                            fic_nonfic_text = fic_nonfic_text,
                            best_tweet_form=best_tweet_form)





