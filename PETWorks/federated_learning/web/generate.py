import base64


def generateWebView(origin, recover, history, similarity):

    template = None
    with open("PETWorks/federated_learning/web/template.html", "r") as f:
        template = f.read()

    originData = base64.b64encode(open(origin, 'rb').read()).decode('utf-8')
    recoverData = base64.b64encode(open(recover, 'rb').read()).decode('utf-8')
    historyData = base64.b64encode(open(history, 'rb').read()).decode('utf-8')

    originImgHtml = '<img src="data:image/png;base64,{0}" style=""width="200; height="200"">'.format(
        originData)
    recoverImgHtml = '<img src="data:image/png;base64,{0}" style=""width="200; height="200"">'.format(
        recoverData)
    historyImgHtml = '<img src="data:image/png;base64,{0}">'.format(
        historyData)

    percentage = int(similarity*100)

    html = template + f"""
    <div class="row"><div class="circle-wrap"><div class="circle">
    <div class="mask full-2"><div class="fill-2"></div></div><div class="mask half">
    <div class="fill-2"></div></div>
    <div class="inside-circle"> {percentage}% </div>
    </div></div></div><main><div class="row">
    <div class="column origin" style="width: 50%;">
    <div class="card">{originImgHtml}<div class="container">
    <h4><b>Original Image</b></h4></div></div></div>
    <div class="column origin" style="width: 50%;">
    <div class="card">{recoverImgHtml}<div class="container">
    <h4><b>Recovered Image</b></h4></div></div></div></div>
    </main><div class="row"><div class="process">
    <h2 class="title" style="font-size: 2.4rem; margin-bottom: 30px">Recover Process</h2>
    {historyImgHtml}</div></div></body></html>
    """
    return html
