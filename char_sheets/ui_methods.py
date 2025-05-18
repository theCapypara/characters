import re


def p(data: any, string: any):
    string = str(string).strip().replace('\n', '<br>')
    if len(string) > 1:
        return string[0].upper() + string[1:]
    return string.upper()


def sp(data: any, val: int):
    if val > 0:
        return '+' + str(val)
    return val


def pab(data: any, string: any):
    return re.sub(
       r"^(.*?):(?:<br>)*(.*$)",
       r'<span class="inline-h3">\1: </span>\2',
       p(data, string)
    )


def up(data: any, string: any):
    return str(string).upper().strip().replace('\n', '<br>')


def size(data: any, feet: int):
    if feet == 30:
        meter = 9
    else:
        meter = round(feet / 3.281, 1)
    return f'''
        <span class="unitc">
            <span class="main">
                <span class="amount">{feet}</span><span class="unit">ft.</span>
            </span>
            <span class="converted">
                (<span class="amount">{meter}</span><span class="unit">m</span>)
            </span>
        </span>'''


def weight(data: any, pound: int):
    kg = round(pound / 2.205, 1)
    return f'''
        <span class="unitc">
            <span class="main">
                <span class="amount">{pound}</span><span class="unit">lbs.</span>
            </span>
            <span class="converted">
                (<span class="amount">{kg}</span><span class="unit">kg</span>)
            </span>
        </span>'''


def round5(x):
    return int(5 * round(float(x)/5))
