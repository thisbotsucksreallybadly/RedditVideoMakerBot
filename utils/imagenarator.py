import re
from TTS.engine_wrapper import process_text
import textwrap

from PIL import Image, ImageDraw, ImageFont
from rich.progress import track


def draw_multiple_line_text(image, text, font, text_color,padding ,wrap=50) -> None : 
    '''
    Draw multiline text over given image
    '''
    draw = ImageDraw.Draw(image)
    Fontperm= font.getsize(text)
    image_width, image_height = image.size
    lines = textwrap.wrap(text, width=wrap)
    
    y=(image_height/2)-(((Fontperm[1]+(len(lines)*padding)/len(lines))*len(lines))/2)
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y),line, font=font, fill=text_color)
        y += line_height + padding

#theme=bgcolor,reddit_obj=reddit_object,txtclr=txtcolor
def imagemaker( theme,
                reddit_obj:dict,
                txtclr,
                padding=5
                ):
    '''
    Render Images for video 
    '''
    title  : str  = process_text(reddit_obj['thread_title'], False)
    texts  : list  = [process_text(s,False) for s in reddit_obj['thread_post']]
    id : str = re.sub(r"[^\w\s-]", "", reddit_obj["thread_id"])

    tfont=ImageFont.truetype("fonts\\Roboto-Bold.ttf",27) # for title
    font=ImageFont.truetype("fonts\\Roboto-Regular.ttf", 20)# for despcription|comments
    size=(500,176) 
    
    image =Image.new('RGBA',size,theme)
    draw = ImageDraw.Draw(image)

    # for title
    if len(title)>40:
        draw_multiple_line_text(image, title,tfont,txtclr ,padding,wrap=30)
    else:
        
        Fontperm= tfont.getsize(title)
        draw.text(((image.size[0]-Fontperm[0])/2,(image.size[1]-Fontperm[1])/2),font=tfont,text=title) #(image.size[1]/2)-(Fontperm[1]/2)
    
    image.save(f'assets/temp/{id}/png/title.png')    

    # for comment|description

    for idx,text in track(enumerate(texts),"Rendering Image"):

        image =Image.new('RGBA',size,theme)
        draw = ImageDraw.Draw(image)

        if len(text)>50:
            draw_multiple_line_text(image, text,font, txtclr,padding)

        else:
            
            Fontperm= font.getsize(text)
            draw.text(((image.size[0]-Fontperm[0])/2,(image.size[1]-Fontperm[1])/2),font=font,text=text) #(image.size[1]/2)-(Fontperm[1]/2)
        image.save(f'assets/temp/{id}/png/img{idx}.png')


if __name__ == "__main__" :
    
    reddit_obj  = {}

    reddit_obj["thread_id"] = 'test'
    reddit_obj['thread_title'] = "something to test for"
    reddit_obj['thread_post'] = 'lorem asd0c vi0di9ds7  8 8ioikj klh  hjhhj o ;h; lkj lkj ;j; klj;lkjl l; jlkl;kj k j;lkj;lkj ' , 'lsdfksl;dfl;s ;sdkfs;lfk '


    imagemaker( ( 45 ,37,47,0),reddit_obj,'white')