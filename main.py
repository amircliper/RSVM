from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import os

def create_rsvp_video(text, font_size, screen_size, word_duration, output_file, font_path, num_prev_words=1):
    # Split text into words
    words = text.split()

    # Create list to store video clips
    clips = []
    temp_files = []

    # Loop through words and create images
    for i in range(len(words)):
        img = Image.new('RGB', screen_size, color=(0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Load font
        font = ImageFont.truetype(font_path, font_size)

        # Get previous, current, and next words
        prev_words = words[max(0, i-num_prev_words):i]
        current_word = words[i]
        next_word = words[i+1] if i < len(words) - 1 else ""

        # Reshape and display text correctly for Arabic/Persian
        reshaped_current_word = arabic_reshaper.reshape(current_word)
        bidi_current_word = get_display(reshaped_current_word)

        # Calculate text sizes
        curr_bbox = draw.textbbox((0, 0), bidi_current_word, font=font)
        curr_text_width = curr_bbox[2] - curr_bbox[0]
        curr_text_height = curr_bbox[3] - curr_bbox[1]

        # Calculate positions
        center_x = screen_size[0] // 2
        center_y = screen_size[1] // 2

        curr_position = (center_x - curr_text_width // 2, center_y - curr_text_height // 2)

        # Draw text on image
        draw.text(curr_position, bidi_current_word, fill=(255, 255, 255), font=font)      # Current word in black

        # Save image to a temporary file
        temp_file = f"{i}_{current_word}.png"
        img.save(temp_file)
        temp_files.append(temp_file)

        # Create video clip from image
        clip = ImageClip(temp_file).set_duration(word_duration)
        clips.append(clip)

    # Concatenate all clips
    final_clip = concatenate_videoclips(clips, method="compose")

    # Write final video to file
    final_clip.write_videofile(output_file, fps=24)

    # Remove temporary files
    for temp_file in temp_files:
        os.remove(temp_file)

# Example usage
text = "است که آن پایین کلی آدم بود ولی او نبود. میتوانست حداقل خداحافظی کند. ولی با این وجود، مالقات دلپذیری بود. برگشتم و پشت میزم نشستم. بعد تلفن را برداشتم و شماره تونی را گرفتم. جواب داد: بله؟ پیتزا فروشی... تونی، آقای اِسلو دث هستم. چی؟ تو هنوز میتونی حرف بزنی؟ من خوب هم حرف میزنم، تونی. هیچ وقت سرحالتر از االن نبودم. من که نمیفهمم... بچههات اومدن اینجا، تونی... جدی؟ جدی؟ این دفعه رو بهشون حال دادم، گذاشتم راحت برن. یه بار دیگه بفرستیشون ترتیبشونو کامل میدم. صدای نفس کشیدن تونی را در گوشی تلفن میشنیدم. با حالتی بسیار سردرگم نفس میکشید. بعد گوشی را گذاشت. یک بطر اسکاچ از کشوی سمت چپ پایین درآوردم، درش را باز کردم و یک جرعه حسابی زدم. سربهسر بلین بگذاری، حسابت صاف است. به همین سادگی. در بطری را بستم، به داخل کشو برگرداندمش و به فکر افتادم که حاال چه باید بکنم. یک کارآگاه خوب همیشه کار برای انجام دادن دارد. توی فیلمها که دیدهاید. یکی در زد. یعنی در واقع پنج تقه سریع به در خورد. بلند، مصرّانه. من همیشه میتوانم در زدن آدمهای مختلف را تشخیص بدهم. بعضی وقتها که تشخیصِ بدی بدهم، در را باز نمیکنم. این در زدن، نیمه بد بود. گفتم: بیا تو. در باز شد. مردی بود پنجاهوخردهای ساله، نیمه پولدار، نیمه عصبی، پاهای خیلی بزرگ، زگیل روی قسمت چپ باالی پیشانی، چشمهای قهوهای، کراوات. دوتا ماشین، دوتا خانه، بدون بچه. استخر و جکوزی، اهل بازی با بازار سهام و دارای بالهت به میزان کافی. همانجا ایستاد، مختصر عرقی کرده بود، و به من خیره شد. گفتم: بنشینید. 1 گفت: جک باس هستم. و... میدونم. چی رو؟ شما فکر میکنین که همسرتون با یک یا چند نفر روابط جنسی داره. بله. همسرتون بیستوچند سالشه. بله. میخوام ثابت کنی که اون این کارو میکنه، بعد طالق میگیرم. چرا به خودت زحمت میدی باس؟ خب، طالقش بده. من فقط میخوام ثابت بشه که اون... اون... فراموشش کن. به هر صورت همونقدر ازت پول میگیره. االن عصر جدیده. یعنی چی؟ بهش میگن طالق توافقی. فارغ از خطا. مهم نیست کی چیکار کرده. چطور؟ خب اینجوری اجرای عدالت سریعتر میشه، دادگاهها خلوتتر میشن. ولی این که عدالت نیست. اونا فکر میکنن هست. باس نفسزنان در صندلیش نشسته بود و مرا نگاه میکرد. من گرفتار حل مسئله سلین و پیدا کردن گنجشک قرمز بودم، آن وقت این توپ گوشت شلوول نگران دادن زنش به غریبهها بود. دوباره به حرف آمد. من فقط میخوام بفهمم. برای خاطر خودم میخوام بفهمم. من قیمت کارم ارزون نیست. چند؟ ساعتی 1 دالر. به نظر که پول زیادی نمیاد. برای من هست. هیچ عکسی از زنت همراهته؟ دست در کیف پولش کرد، عکسی درآورد و به من داد. عکس را نگاه کردم. یا خدا! واقعاً این شکلیه؟ بله. من که با همین یه نگاه شق کردم. هی، هیز بازی درنیار! آخ، شرمنده... ولی من باید عکس رو نگه دارم. کارم که تموم شد برش میگردونم. عکس را در کیف پولم گذاشتم. هنوز با تو زندگی میکنه؟ بله. و تو میری سر کار؟ بله. و بعد، بعضی وقتا، اون... بله. و چی باعث شده فکر کنی که اون... نکتههای ریز، تماسهای تلفنی، صداهای توی سرم، عوض شدن رفتارش، هزارتا چیز. کاغذ یادداشتی به سمت او هل دادم. آدرس خونه و محل کار، تلفن خونه و محل کار رو بنویس. از اینجا به بعدش با من. خشتکشو پرچم میکنم. پرده از کل ماجرا برمیدارم. چی؟ من دارم پروندهات رو قبول میکنم آقای باس. وقتی به ثمر رسید خبرت میکنم. پرسید: به ثمر رسید؟ ببین، تو حالت خوبه؟ من خوبم. شما چطور؟ آه، آره، منم خوبم. پس نگران نباش. من آدم توام. خشتکشو پرچم میکنم! باس آرام از روی صندلی بلند شد. به سمت در رفت و بعد برگشت. بارتون سفارشت کرده! پس خیالت تخت! عصرت بخیر، آقای باس. در بسته شد و رفت. بارتون پیر نازنین. عکس زن را از کیفم بیرون آوردم و تماشا کردم. فکر کردم، ای جنده، ای جنده. بلند شدم و در را قفل کردم، بعد گوشی را از روی تلفن برداشتم. پشت میزم نشستم و عکس را تماشا کردم. فکر کردم، ای جنده، خشتکتو پرچم میکنم! پرچم! بخششی در کار نیست! رو کار میگیرمت! ای جنده، ای هرزه، ای جنده! نفسم سنگین شد. زیپم را باز کردم. بعد دیگر زلزله شد. عکس را انداختم و زیر میز چمباتمه زدم. حال داد. خوب بود. فکر کنم دو دقیقهای طول کشید. بعد تمام شد. از زیر میز بیرون آمدم، زیپم هنوز باز بود. عکس را پیدا کردم، به داخل کیف بغلیام برش گرداندم، زیپم را بستم. سکس همهاش دام بود، تله بود. برای حیوانات. من شعورم بیشتر از این گند و کثافتکاریها بود. گوشی تلفن را سر جایش گذاشتم، در را باز کردم، بیرون رفتم، قفلش کردم و به سمت آسانسور رفتم. کلی کار داشتم که باید انجام میدادم. من بهترین کارآگاه خصوصی کل لسآنجلس و هالیوود بودم. دکمه را زدم و منتظر پایین آمدن آسانسور کوفتی ماندم."
text = text.replace('/','')
text = text.replace(':','')
font_size = 50
font_path = 'Vazir.ttf'
screen_size = (1280, 1280)  # 1:1 aspect ratio
word_duration = 0.25  # Duration for each word in seconds
output_file = "rsvp_video_07.mp4"
num_prev_words = 4  # Number of previous words to show

create_rsvp_video(text, font_size, screen_size, word_duration, output_file, font_path, num_prev_words)
