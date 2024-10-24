import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import os

model = YOLO('appleyolo11s(3).pt')

disease_info = {
    'alternaria': {
        'description': 'Альтернариоз — грибковая болезнь, возбудителем которого является гриб Alternaria mali Roberts.',
        'treatment': 'Фунгициды - "«Топсин-м СП», Триадимефон, Дифеноконазол, ХОМ, Тебуконазол, Сера коллоидная, Пенконазол (Топаз), Кэптан, Bacillus subtilis штамм В-10 ВИЗР «Альбит»,Смесь Бордоская, «Хорус», Bacillus subtilis штамм М-22 ВИЗР',
        'prevention': 'Профилактика включает использование устойчивых к заболеванию сортов, проведение санитарных мероприятий направленных на снижение запаса инфекции, а также проведение химических обработок.'
    },
    'anthracnose': {
        'description': 'Антракноз — это грибковое заболевание, возбудителем которого являются грибы из рода Neofabrea.',
        'treatment': 'Фунгициды - "«Топсин-м СП», Триадимефон, Дифеноконазол, ХОМ, Тебуконазол, Сера коллоидная, Пенконазол (Топаз), Кэптан, Bacillus subtilis штамм В-10 ВИЗР «Альбит»,Смесь Бордоская, «Хорус», Bacillus subtilis штамм М-22 ВИЗР',
        'prevention': 'Использование устойчивых к заболеванию сортов, проведение санитарных мероприятий направленных на снижение запаса инфекции, а также проведение химических обработок.'
    },
    'marssonina': {
        'description': 'Марссония —  это опасное заболевание яблони, которое приводит к полному осыпанию листьев.',
        'treatment': 'Дезинфекция. После снятия укрытия и перед укрытием нужно обработать растения неразбавленным отбеливателем «Белизна». Для этого подойдёт 3% раствор железного или 2% раствор медного купороса. Обработка салициловой кислотой. После того как отрастающие побеги окрепнут, но до появления тёмно-зелёных листьев, нужно обработать растения 2% спиртовым раствором салициловой кислоты. Для этого 100 мл раствора растворяют в 10 л воды и при желании добавляют столовую ложку нашатырного спирта. Обработка медьсодержащими препаратами. Её проводят после появления первых бутонов. Медьсодержащие обработки и опрыскивания для стимуляции фитоиммунитета чередуют через неделю.',
        'prevention': 'Использование устойчивых к заболеванию сортов, проведение санитарных мероприятий направленных на снижение запаса инфекции, а также проведение химических обработок.'
    },
    'scab': {
        'description': 'Парша — заболевание и повреждения на листьях и плодах яблони, вызываемые сумчатым грибом Venturia inaequalis.',
        'treatment': 'Для лечения парши можно использовать специализированные средства, такие, например, как «Бордоская жидкость» и «Раёк». Применять препараты следует точно в соответствии с предписаниями производителя.',
        'prevention': 'В целях профилактики парши яблонь нужно придерживаться следующих правил: не высаживать деревья слишком близко друг к другу сплошными рядами, регулярно выполнять обрезку веток, обеспечивая яблоню необходимым количеством тепла и света, по возможности выбирать более устойчивые к заболеванию сорта.'
    },
    'sootyblotch': {
        'description': 'Черная пятнистость — дефицит питательных веществ, болезни, кольцевая пятнистость',
        'treatment': 'При дефиците питательных веществ (марганца и магния) лечение заключается во внесении удобрений. В начале периода вегетации нужно подкормить яблоню под корень раствором сульфата магния (на 10 литров воды — 25 г удобрений). Если дождей летом мало, а температура держится выше +25 °С большую часть дня, подойдёт внекорневая подкормка раствором сульфата магния (на 10 л воды — 15 г удобрения). Если дереву не хватает марганца, нужно использовать соответствующее удобрение. При чёрном раке лечение начинается с удаления поражённых частей яблони. Раны, которые остались после болезни, необходимо продезинфицировать (подойдёт пятипроцентный раствор железного купороса) и замазать «Благосадом», пастой «РанНет» или садовым варом. После цветения яблоню нужно обработать однопроцентной бордоской жидкостью, повторить обработку через месяц. Также можно использовать народные методы лечения. Очищенные места можно обработать раствором хозяйственного мыла, солёной водой с йодом, соком свежего щавля или раствором марганцовки.',
        'prevention': 'Использование устойчивых к заболеванию сортов, проведение санитарных мероприятий направленных на снижение запаса инфекции, а также проведение химических обработок.'
    },
    'valsacanker': {
        'description': 'Вальса канкер — болезнь яблони, вызываемая грибком Valsa mali.',
        'treatment': 'Для лечения можно использовать фунгициды или бактерициды, но часто единственным доступным методом является уничтожение заражённого растения, чтобы сдержать распространение болезни.',
        'prevention': 'Использование устойчивых к заболеванию сортов, проведение санитарных мероприятий направленных на снижение запаса инфекции, а также проведение химических обработок.'
    },
    'whiterot': {
        'description': 'Белая гниль — это заболевание, вызываемое грибком Botryosphaeria dothidea.',
        'treatment': 'Для борьбы с белой гнилью рекомендуется удалять и уничтожать поражённые части дерева, а также мумифицированные плоды.',
        'prevention': 'Для профилактики можно использовать устойчивые к болезни сорта, проводить санитарные мероприятия, направленные на снижение запаса инфекции (включая сбор и уничтожение поражённых плодов), а также химические обработки.'
    }
}

def process_image(image):
    # Преобразование изображения в формат, подходящий для модели
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    results = model.predict(img)
    
    # Обработка результатов
    for result in results:
        boxes = result.boxes.cpu().numpy()
        for box in boxes:
            r = box.xyxy[0].astype(int)
            cv2.rectangle(img, r[:2], r[2:], (0, 255, 0), 2)
            cv2.putText(img, model.names[box.cls[0]], (r[0], r[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # Перевод изображения обратно в формат RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img, results

def main():
    st.title("Детекция болезней яблони")
    
    # Выбор изображения из папки test_images или загрузка пользовательского изображения
    test_images_folder = 'test_images'
    test_images = [f for f in os.listdir(test_images_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    selected_image = st.selectbox("Выберите тестовое изображение", test_images)
    
    uploaded_file = st.file_uploader("Загрузите свое изображение", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Загруженное изображение', use_column_width=True)
        
        if st.button('Детектировать болезни на загруженном изображении'):
            processed_image, results = process_image(image)
            st.image(processed_image, caption='Результат детекции', use_column_width=True)
            
            # Информация о болезни
            detected = False
            for result in results:
                boxes = result.boxes.cpu().numpy()
                for box in boxes:
                    class_id = int(box.cls[0])
                    confidence = box.conf[0]
                    class_name = model.names[class_id]
                    if confidence >= 0.95:
                        st.write(f"Болезнь: {class_name}, Уверенность: {confidence:.2f}")
                        detected = True

                        # Вывод дополнительной информации
                        if class_name in disease_info:
                            st.subheader(f"Информация о {class_name}")
                            st.write(f"**Описание:** {disease_info[class_name]['description']}")
                            st.write(f"**Лечение:** {disease_info[class_name]['treatment']}")
                            st.write(f"**Профилактика:** {disease_info[class_name]['prevention']}")
                        else:
                            st.write("Дополнительная информация отсутствует.")
            if not detected:
                st.write("Болезни не обнаружены.")
    elif selected_image:
        image_path = os.path.join(test_images_folder, selected_image)
        image = Image.open(image_path)
        st.image(image, caption='Выбранное изображение', use_column_width=True)
        
        if st.button('Детектировать болезни'):
            processed_image, results = process_image(image)
            st.image(processed_image, caption='Результат детекции', use_column_width=True)
            
            # Информация о болезни
            detected = False
            for result in results:
                boxes = result.boxes.cpu().numpy()
                for box in boxes:
                    class_id = int(box.cls[0])
                    confidence = box.conf[0]
                    class_name = model.names[class_id]
                    if confidence >= 0.95:
                        st.write(f"Болезнь: {class_name}, Уверенность: {confidence:.2f}")
                        detected = True

                        # Вывод дополнительной информации
                        if class_name in disease_info:
                            st.subheader(f"Информация о {class_name}")
                            st.write(f"**Описание:** {disease_info[class_name]['description']}")
                            st.write(f"**Лечение:** {disease_info[class_name]['treatment']}")
                            st.write(f"**Профилактика:** {disease_info[class_name]['prevention']}")
                        else:
                            st.write("Дополнительная информация отсутствует.")
            if not detected:
                st.write("Болезни не обнаружены.")

if __name__ == "__main__":
    main()
