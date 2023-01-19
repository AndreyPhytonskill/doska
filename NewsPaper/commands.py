from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment

# для проставления лайков/дислайков. 
import random 

def todo():    
    # полезно для отладки удалять объекты
    User.objects.all().delete()
    Category.objects.all().delete()
    
    # создание пользователей
    name1_user = User.objects.create_user(username = 'username', email = 'username1@mail.ru', password = 'name1_password')
    name2_user = User.objects.create_user(username = 'username2', email = 'username2@mail.ru', password = 'name2_password')
    
    # создание объектов авторов
    name1 = Author.objects.create(user = name1_user)
    name2 = Author.objects.create(user = name2_user)
    
    # создание категорий
    cat_tex = Category.objects.create(name = "Техника")
    cat_cin= Category.objects.create(name = "Наука")
    cat_sport = Category.objects.create(name = "Спорт")
    cat_IT = Category.objects.create(name = "IT")
    
    # создание текстов статей/новостей
    text_article_sport_cin = """Бег — один из способов передвижения (локомоции) человека и животных; 
                                     отличается наличием так называемой «фазы полёта» и осуществляется в 
                                         результате сложной координированной деятельности скелетных мышц и конечностей."""
    
    text_article_sport = """Дзюдо́ (яп. 柔道 дзю: до:, дословно — «Мягкий путь»; в России также часто используется вариант перевода «Гибкий путь»)
                             — японское боевое искусство, философия и спортивное единоборство без оружия, созданное в конце XIX века на основе дзюдзюцу 
                              японским мастером боевых искусств Дзигоро Кано (яп. 嘉納 治五郎 Кано: Дзигоро: 1860 — 1938), 
                              который также сформулировал основные правила и принципы тренировок и проведения состязаний."""
    
    text_news_IT = """Для того чтобы добиться успехов в этой сфере необходимо правильно подойти к вопросу образования. 
                       Сегодня существует огромное множество онлайн ресурсов, которые помогут вам построить карьеру в IT-индустрии. 
                        В этой статье мы расскажем о том, на какие онлайн курсы программирования необходимо обратить внимание в 2023 году."""
    
    # создание двух статей и новости
    article_name1 = Post.objects.create(author = name1, post_type = Post.article, title = "Бег", text = text_article_sport_cin)
    article_name2 = Post.objects.create(author = name2, post_type = Post.article, title = "Дзюдо", text = text_article_sport)
    news_name2 = Post.objects.create(author = tommy, post_type = Post.news, title = "Программирование на Python с нуля", text = text_news_IT)
    
    # присваивание категорий этим объектам
    PostCategory.objects.create(post = article_name1, category = cat_sport)
    PostCategory.objects.create(post = article_name1, category = cat_cin)
    PostCategory.objects.create(post = article_name2, category = cat_sport)
    PostCategory.objects.create(post = news_name2, category = cat_IT)
    
    # создание комментариев
    comment1 = Comment.objects.create(post = article_name1, user = name2.user, text = "Очень интересно!")
    comment2 = Comment.objects.create(post = article_name2, user = name1.user, text = "Занимательно")
    comment3 = Comment.objects.create(post = news_name2, user = name1.user, text = "Класс!)
    comment4 = Comment.objects.create(post=article_name1, user=name2.user, text="Вперед")
    comment5 = Comment.objects.create(post=article_name2, user=name1.user, text="Так держать")
    
    
    # список всех объектов, которые можно лайкать
    list_for_like = [article_name1,
                    article_name2,
                    news_name2,
                    comment1,
                    comment2,
                    comment3,
                    comment4,
                    comment5
                     ]
    
    # 100 рандомных лайков/дислайков (по четности счетчика)
    for i in range(100):
        random_obj = random.choice(list_for_like)
        if i % 2:
            random_obj.like()
        else:
            random_obj.dislike()
            
    # подсчет рейтинга 
    rating_name1 = (sum([post.rating*3 for post in Post.objects.filter(author=johny)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(user=johny.user)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(post__author=johny)]))
    name1.update_rating(rating_johny) # и обновление
    
    # подсчет рейтинга 
    rating_name2 = (sum([post.rating*3 for post in Post.objects.filter(author=tommy)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(user=tommy.user)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(post__author=tommy)]))
    name2.update_rating(rating_tommy) # и обновление
    
    # лучший автор
    best_author = Author.objects.all().order_by('-rating')[0]
    
    print("Лучший автор")
    print("username:", best_author.user.username)
    print("Рейтинг:", best_author.rating)
    print("")
    
    # лучшая статья(!) 
    best_article = Post.objects.filter(post_type = Post.article).order_by('-rating')[0]
    print("Лучшая статья")
    print("Дата:", best_article.time)
    print("Автор:", best_article.author.user.username)
    print("Рейтинг:", best_article.rating)
    print("Заголовок:", best_article.title)
    print("Превью:", best_article.preview())
    print("")
    
    # печать комментариев к ней. Обязательно цикл, потому что комментарий может быть не один и нужен универсальный код
    print("Комментарии к ней")
    for comment in Comment.objects.filter(post = best_article):
        print("Дата:", comment.time)
        print("Автор:", comment.user.username)
        print("Рейтинг:", comment.rating)
        print("Комментарий:", comment.text)
        print("")