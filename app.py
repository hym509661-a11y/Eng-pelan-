import streamlit as st
import pygame
import random

# إعداد واجهة Streamlit
st.set_page_config(page_title="Qamishli Racing Game", layout="centered")
st.title("🚗 سباق شوارع القامشلي (Qamishli Drive)")
st.info("استخدم أسهم الكيبورد (يمين ويسار) لتجنب الحواجز في شوارع المدينة")

# كود اللعبة باستخدام Pygame
def start_game():
    pygame.init()
    width, height = 400, 600
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # ألوان وإعدادات
    car_x = width // 2
    car_y = height - 100
    car_speed = 5
    obstacle_x = random.randint(0, width - 50)
    obstacle_y = -100
    score = 0

    running = True
    while running:
        screen.fill((50, 50, 50))  # لون الطريق (أسفلت)
        
        # رسم خطوط الطريق (محاكاة شوارع القامشلي)
        pygame.draw.rect(screen, (255, 255, 255), (width//2 - 5, 0, 10, height))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # التحكم
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 0:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < width - 50:
            car_x += car_speed

        # حركة العوائق
        obstacle_y += 7
        if obstacle_y > height:
            obstacle_y = -100
            obstacle_x = random.randint(0, width - 50)
            score += 1

        # رسم السيارة والعوائق
        pygame.draw.rect(screen, (0, 255, 0), (car_x, car_y, 50, 80)) # سيارتك
        pygame.draw.rect(screen, (255, 0, 0), (obstacle_x, obstacle_y, 50, 50)) # سيارة أخرى

        # كشف الاصطدام
        if (car_y < obstacle_y + 50 and car_y + 80 > obstacle_y and 
            car_x < obstacle_x + 50 and car_x + 50 > obstacle_x):
            running = False

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    return score

# تشغيل اللعبة داخل Streamlit
if st.button("ابدأ اللعب الآن"):
    final_score = start_game()
    st.warning(f"انتهت اللعبة! مجموع النقاط في شوارع القامشلي: {final_score}")

# التذييل الخاص بك
st.markdown("---")
st.write("للتواصل والدعم الفني: **0998449697**")
