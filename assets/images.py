import os

import requests
from PIL import Image, ImageFont, ImageDraw, ImageFilter


async def draw_song_interface(name, time, artist, thumbnail_size, cover: str):
    song_cover_image = Image.open(requests.get(cover, stream=True).raw)
    decoration = Image.open("assets/playing_deco.png")

    # Create a modern interface image
    width, height = 800, 200

    # Convert the song cover image to RGBA mode
    song_cover_image = song_cover_image.convert("RGBA")

    bg_cover = song_cover_image.copy()

    # Create an empty RGBA image
    modern_interface_image = Image.new("RGBA", (width, height), (2, 4, 3))

    cover_resized = bg_cover.resize((width, height + 500))

    # Paste the song cover thumbnail on the side
    modern_interface_image.paste(
        cover_resized.filter(ImageFilter.GaussianBlur(3)),
        ((width - cover_resized.width) // 2, (height - cover_resized.height) // 2)
    )

    decoration = decoration.resize((660, 220))

    modern_interface_image.paste(decoration, (
        (width - decoration.width) // 2,
        (height - decoration.height) // 1), decoration)

    # Draw additional elements (title, time, etc.) on the other side
    font_size = 30 - (len(name) // 3)
    font = ImageFont.truetype(
        os.path.join(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__), ".."
                )
            ),
            "FiraSans-Bold.ttf"
        ),
        font_size
    )

    font_small = ImageFont.truetype(
        os.path.join(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__), ".."
                )
            ),
            "FiraSans-Light.ttf"
        ),
        25
    )

    total_seconds = time // 1000

    # Calculate hours, minutes, and seconds
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    draw = ImageDraw.Draw(modern_interface_image)

    text_track_name_pos = (300 - len(name) // 3, height - 180)
    text_time_name_pos = (35, height - 50)

    text_name = f"{artist} - {name}"
    time_text = f"{minutes}:{seconds}"

    shadow_offset = 2
    shadow_position_name = (text_track_name_pos[0] + shadow_offset, text_track_name_pos[1] + shadow_offset)
    shadow_position_time = (text_time_name_pos[0] + shadow_offset, text_time_name_pos[1] + shadow_offset)

    draw.text(shadow_position_name, text_name, font=font, fill="black")
    draw.text(shadow_position_time, time_text, font=font_small, fill="black")
    draw.text(text_track_name_pos, text_name, fill="white", font=font)
    draw.text(text_time_name_pos, time_text, fill="white", font=font_small)

    # Save the image to a temporary file
    image_path = "modern_interface.png"
    modern_interface_image.save(image_path)

    return image_path
