from flask import Flask, render_template, request
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import os

UPLOAD_FOLDER = 'static/uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

classes = ['Asthma Plant', 'Avaram', 'Coatbuttons', 'Heart-Leaved Moonseed', 'Indian Jujube', 'Malabar Catmint', 'Mexican Mint', 'Panicled Foldwing', 'Prickly Chaff Flower', 'Punarnava', 'Rosary Pea', 'Sweet Flag', 'Tinnevelly Senna', 'Trellis Vine', 'Velvet Bean']
sym = {
    'Asthma Plant': 'Euphorbia hirta',
    'Avaram': 'Senna auriculata',
    'Coatbuttons': 'Tridax procumbens',
    'Heart-Leaved Moonseed': 'Tinospora cordifolia',
    'Indian Jujube': 'Ziziphus mauritiana',
    'Malabar Catmint': 'Anisomeles malabarica',
    'Mexican Mint': 'Coleus amboinicus',
    'Panicled Foldwing': 'Dicliptera paniculata',
    'Prickly Chaff Flower': 'Achyranthes aspera',
    'Punarnava': 'Boerhavia diffusa',
    'Rosary Pea': 'Abrus precatorius',
    'Sweet Flag': 'Acorus calamus',
    'Tinnevelly Senna': 'Senna alexandrina',
    'Trellis Vine': 'Wisteria macrostachya',
    'Velvet Bean': 'Mucuna pruriens.'
}
ferti = {
    'Asthma Plant': 'Euphorbia is used for breathing disorders including asthma, bronchitis, and chest congestion.',
    'Avaram': 'prevents bacterial growth and is also effective in curing infections',
    'Coatbuttons': 'Useful in jaundice, bronchial catarrh, diarrhoea, dysentery, inflammation, ulcers, anal fistula, and hemorrhoids',
    'Heart-Leaved Moonseed': 'the plant is of great interest to researchers across the globe because of its reported medicinal properties like anti-diabetic, anti-periodic, anti-spasmodic, anti-inflammatory, anti-arthritic, anti-oxidant, anti-allergic, anti-stress',
    'Indian Jujube': 'A powerhouse of antioxidants jujube fruits are well known to enhance skin health, detoxifies the blood and improves cardiac function',
    'Malabar Catmint': 'folkloric medicine to treat amentia, anorexia, fevers, swellings, rheumatism',
    'Mexican Mint': 'improve the health of your skin, detoxify the body, defend against colds, ease the pain of arthritis, relieve stress and anxiety, treat certain kinds of cancer, and optimize digestion',
    'Panicled Foldwing': 'leaves bestowed with essential minerals and vitamins helps to soothe the upset gut, treats asthma, common cold and sore throat',
    'Prickly Chaff Flower': 'Achyranthes Aspera is used in the treatment of boils, asthma, in facilitating delivery, bleeding, bronchitis, debility, dropsy, cold.',
    'Punarnava': 'The herb can be used as a diuretic in case of renal failure, or as an astringent in bleeding disorders',
    'Rosary Pea': 'The roots, leaves, and seeds of jequirity plant are used in various forms to cure wide-ranging health problems, from leprosy to snake bites',
    'Sweet Flag': 'It is useful in the treatment of bronchitis, fevers, and general debility, and is sometimes given for increasing the appetite and benefiting digestion',
    'Tinnevelly Senna': 'This plant is used for the treatment of inflammatory diseases and liver problems',
    'Trellis Vine': 'Wisteria flowers are also edible and offer a sweet scent and taste. They are sometimes used in traditional Chinese medicine',
    'Velvet Bean': 'Velvet bean is used for diabetes, painful menstruation, increasing sexual desire, and for starting menstruation in women with amenorrhea'
}

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            img = image.load_img(filepath, target_size=(150, 150))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            model = load_model('model.h5')
            result = model.predict(img)
            predicted_class = classes[np.argmax(result)]
            scientific_name = sym.get(predicted_class)
            fertilizer = ferti.get(predicted_class)
            return render_template('result.html', filename=filename, predicted_class=predicted_class, scientific_name=scientific_name, fertilizer=fertilizer)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
