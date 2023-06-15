# parse different PDU lines and save them by series into Excel files
# bare "except" used intentionally to simplify
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd


# function to parse link of exact model to get model name and all the required specs. return all the specs as str vars
def parse_link(url_input):
    response = requests.get(url_input)
    soup_text_lxml = BeautifulSoup(response.text, 'lxml')

    model1 = str(soup_text_lxml).split("page_id: \"")[1].split('"')[0]

    # noinspection PyBroadException
    try:
        phase1 = (str(soup_text_lxml).split('Количество фаз на входе</td><td class="specValue">')[1].split('</td>')[0])
    except:
        phase1 = 'не найдено'

    # noinspection PyBroadException
    try:
        current1 = \
            (str(soup_text_lxml).split('Максимальный входной ток</td><td class="specValue">')[1].split('</td>')[0])
    except:
        current1 = 'не найдено'

    # noinspection PyBroadException
    try:
        input_plug1 = \
            (str(soup_text_lxml).split('Тип входного подключения</td><td class="specValue">')[1].split('</td>')[0])
    except:
        # noinspection PyBroadException
        try:
            input_plug1 = (str(soup_text_lxml).split('Тип вилки PDU</td><td class="specValue">')[1].split('</td>')[0])
        except:
            input_plug1 = 'не найдено'

    # noinspection PyBroadException
    try:
        output_plugs1 = (str(soup_text_lxml).split('Выходные розетки</td><td class="specValue">')[1].split('</td>')[0])
    except:
        output_plugs1 = 'не найдено'

    # noinspection PyBroadException
    try:
        breakers1 = (str(soup_text_lxml).split('Защита от перегрузки</td><td class="specValue">')[1].split('</td>')[0])
    except:
        breakers1 = 'не найдено'

    # noinspection PyBroadException
    try:
        form_factor1 = \
            (str(soup_text_lxml).split('Поддерживаемые форм-факторы</td><td class="specValue">')[1].split('</td>')[0])
    except:
        form_factor1 = 'не найдено'

    # noinspection PyBroadException
    try:
        op_temp1 = \
            (str(soup_text_lxml).split('Диапазон рабочих температур</td><td class="specValue">')[1].split('</td>')[0])
    except:
        op_temp1 = 'не найдено'

    return model1, phase1, current1, input_plug1, output_plugs1, breakers1, form_factor1, op_temp1


baseurl = 'http://'  # personal data. remove when git, baseurl to form links to exact models

# Create a new driver.
driver = webdriver.Chrome()

# 1st stage. parse page with all the models of the serie

# Navigate to the page.
# personal data. remove when git
# here were the links to the different series
# uncomment one link at time to save another series
# driver.get('https://') # basic (basic)
# driver.get('https://') # local metered (monitored)
# driver.get('https://') # monitored (monitored)
# driver.get('https://') # switched (switched)
# driver.get('https://') # managed (Sw-M-b-O)

# Get the HTML content of the page.
page_content = driver.page_source

# Close the driver.
driver.close()

# Parse the page with BeautifulSoup.
soup = BeautifulSoup(page_content, 'html.parser')

# 2nd stage - get all the links to all the models of the serie from soup

links = (str(soup).split('" rel="noopener" target="_blank"><span class="itemNumber"'))

# form lists to save specs
models = []
phases = []
currents = []
input_plugs = []
output_plugss = []
breakerss = []
form_factors = []
op_temps = []
urls = []

# parse each model webpage and save specs into lists
for link in links[:-1]:
    # print (link)
    # print (link.split('" data-source="category" href="/')[:-1])
    # print (baseurl +  (link.split('data-source="category" href="/')[-1]) )
    url = (baseurl + (link.split('data-source="category" href="/')[-1]))
    model, phase, current, input_plug, output_plugs, breakers, form_factor, op_temp = parse_link(url)

    models.append(model)
    phases.append(phase)
    currents.append(current)
    input_plugs.append(input_plug)
    output_plugss.append(output_plugs)
    breakerss.append(breakers)
    form_factors.append(form_factor)
    op_temps.append(op_temp)
    urls.append(url)
    pass

# Create a Pandas DataFrame from list of all the models of one serie
df = pd.DataFrame({
    "Model": models,
    "Phase": phases,
    "Current": currents,
    "Input Plug": input_plugs,
    "Output Plugs": output_plugss,
    "Breakers": breakerss,
    "Form Factor": form_factors,
    "Operating Temperature": op_temps,
    "URL": urls

})

# Save the DataFrame to an Excel file
# uncomment each line corresponded to link of series
# df.to_excel("basic.xlsx")
# df.to_excel("managed.xlsx")
# df.to_excel("local_metered.xlsx")
# df.to_excel("monitored.xlsx")
# df.to_excel("switched.xlsx")
# df.to_excel("managed.xlsx")
print("done")
