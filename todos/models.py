from django.db import models
from django.conf import settings

# Create your models here.
class ToDO(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name= 'todos',
        null=True,
        blank= True,
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>template using grid and flexbox</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Balsamiq+Sans&family=Raleway:ital,wght@0,100..900;1,100..900&display=swap"
        rel="stylesheet">
    <style>
        * {
            font-family: Raleway, sans-serif;
            background-color: rgb(204, 200, 200);
            box-sizing: border-box;
            margin: 0px;
            padding: 0px;
        }

        .para {
            font-size: 20px;
            margin-bottom: 80px;

        }

        .first {
            margin-top: 60px;
            margin-bottom: 30px;
        }

        .spa {
            background-color: black;
            color: aliceblue;
            padding: 5px;
        }

        .container {
            height: 1330px;

            display: grid;
            grid-template-columns: 3fr 2fr;
            grid-template-rows: 4fr 1fr 3fr 2fr;
        }

        .box1 {

            grid-row: span 2;
            margin: 15px;
            box-shadow: 5px 5px 5px 5px rgb(178, 173, 173);
            background-color: rgb(240, 240, 240);

        }

        .box2 {

            margin: 15px;
            box-shadow: 5px 5px 5px 5px rgb(178, 173, 173);
            background-color: rgb(240, 240, 240);

        }

        .box3 {

            grid-row: span 2;
            margin: 15px;
            box-shadow: 5px 5px 5px 5px rgb(178, 173, 173);
            background-color: rgb(240, 240, 240);

        }

        .box4 {

            grid-row: span 2;
            margin: 15px;
            box-shadow: 5px 5px 5px 5px rgb(178, 173, 173);
            background-color: rgb(240, 240, 240);

        }

        .box5 {

            margin: 15px;
            box-shadow: 5px 5px 5px 5px rgb(178, 173, 173);
            background-color: rgb(240, 240, 240);

        }

        .inner {
            margin: 20px;
            background-color: rgb(240, 240, 240);
        }

        .font_ {
            font-size: 20px;
            margin-top: 15px;
            background-color: rgb(240, 240, 240);
        }

        .font1 {
            font-size: 18px;
            margin-top: 20px;
            background-color: rgb(240, 240, 240);
        }

        .inner1 {
            display: flex;
            justify-content: space-between;
            margin: 20px;
            background-color: rgb(240, 240, 240);
        }

        .button {
            height: 50px;
            width: 170px;
            font-size: 18px;
            background-color: rgb(240, 240, 240);
        }

        .button:hover {
            background-color: rgb(190, 182, 182);
        }

        .comm {
            font-size: 23px;
            gap: 20px;
            padding-top: 15px;
            background-color: rgb(240, 240, 240);
        }

        .black {
            background-color: black;
            color: white;
            padding: 5px;
            border-radius: 60%;
        }

        .second {
            margin: 20px;
            background-color: rgb(240, 240, 240);
        }

        .para1 {
            font-size: 18px;
            background-color: rgb(240, 240, 240);
            margin-top: 20px;
        }


        .one {

            background-color: rgb(190, 182, 182);

        }


        .two {
            background-color: rgb(240, 240, 240);
        }

        .three {
            background-color: rgb(240, 240, 240);
        }

        .four {
            background-color: rgb(240, 240, 240);
        }

        .five {
            background-color: rgb(240, 240, 240);
        }

        .t3 {
            font-size: 25px;
            margin-top: 35px;
            margin-left: 20px;
            background-color: rgb(190, 182, 182);
            margin-bottom: 20px;
        }

        .box55 {
            display: grid;
            grid-template-columns: 1fr;
            grid-template-rows: 1fr 3fr;
            background-color: rgb(240, 240, 240);
        }

        .five1 {

            background-color: rgb(190, 182, 182);
        }

        .five2 {

            display: flex;
            flex-wrap: wrap;
            padding: 25px;
            background-color: rgb(240, 240, 240);
        }

        .same {
            background-color: rgb(190, 182, 182);
            padding-top: 5px;
            padding-left: 5px;
            padding-right: 5px;

            margin: 4px;
        }

        .lasst {
            font-size: 25px;
            padding-top: 17px;
            padding-left: 17px;
            padding-bottom: 17px;
            background-color: rgb(190, 182, 182);
        }

        .big {
            display: grid;
            grid-template-columns: 1fr;
            grid-template-rows: 1.5fr 1.5fr 1.5fr 1.5fr 1.5fr;
        }

        .contain {
            display: flex;
            gap: 20px;
            padding-top: 20px;
            padding-left: 20px;
            padding-bottom: 10px;
            background-color: rgb(240, 240, 240);
        }

        .hi {
            background-color: rgb(240, 240, 240);
        }

        .tt {
            margin-top: 10px;
            background-color: rgb(240, 240, 240);
        }

        .two2 {
            background-color: rgb(240, 240, 240);
        }

        .same1 {
            background-color: black;
            color: white;
            padding-top: 5px;
            padding-left: 5px;
            padding-right: 5px;

            margin: 4px;
        }

        .footer {
            height: 200px;
            background-color: #616161;
            position: relative;
        }
        .foot{
            position: absolute;
            top:50px;
            left:50px;
            display: flex;
            gap: 30px;
            background-color: #616161;

        }
        .bot{
            position: absolute;
            top: 150px;
            left: 50px;
            background-color: #616161;
            color: white;
            
        }
        .button1 {
            height: 50px;
            width: 140px;
            font-size: 18px;
            background-color: #9b9898;
            color: white;
        }
        .button2 {
            height: 50px;
            width: 140px;
            font-size: 18px;
            background-color: #000;
            color: white;
        }
    </style>

</head>

<body>
    <center>
        <h1 class="first">MY BLOG</h1>
    </center>
    <center>
        <p class="para">Welcome to the blog of <span class="spa">unknown</span></p>
    </center>
    <div class="container">
        <div class="box1">
            <img src="./food_gallery/woods.jpg" alt="" width="855px" height="300px">
            <div class="inner">
                <h1 class="hi">TITLE HEADING</h1>
                <p class="font_">Title description April 6,2024</p>
                <p class="font1"> Lorem ipsum, dolor sit amet consectetur adipisicing elit. Autem necessitatibus vitae
                    repellat exercitationem. Voluptas vitae tempore nisi nostrum consequatur eveniet neque impedit hic
                    tenetur qui minima commodi nobis magni distinctio modi debitis quod, minus maxime voluptate ea.
                    Cupiditate perferendis veritatis inventore animi iste praesentium aperiam, nisi at quidem doloribus
                    maxime!</p>

            </div>
            <div class="inner1">
                <div> <button class="button">Read More >></button></div>
                <div class="comm">
                    Comments
                    <span class="black">0</span>
                </div>
            </div>
        </div>
        <div class="box2">
            <img src="./food_gallery/avatar_g.jpg" alt="" width="560px" height="300px">
            <div class="second">
                <h2 class="hi">MY NAME</h2>
                <p class="para1">Lorem, ipsum dolor sit amet consectetur adipisicing elit. Dolorem amet mollitia
                    accusantium numquam voluptate dolor ex, temporibus debitis necessitatibus exercitationem fugit iure
                    a sunt optio ad ab at illo harum?
                </p>
            </div>
        </div>
        <div class="box3">
            <div class="big">
                <div class="one">
                    <p class="t3">Popular Posts</p>
                    
                </div>
                <div class="two">
                    <div class="contain">
                        <div class="hi"><img src="./food_gallery/workshop.jpg" alt="" srcset="" height="65px"
                                width="60px"></div>
                        <div class="hi">
                            <p class="two2">Lorem</p>
                            <p class="tt">Sed mattis nunc</p>
                        </div>

                    </div>
                    <hr>

                </div>
                <div class="three">
                    <div class="contain">
                        <div class="hi"><img src="./food_gallery/gondol.jpg" alt="" srcset="" height="65px"
                                width="60px"></div>
                        <div class="hi">
                            <p class="two2">Ipsum</p>
                            <p class="tt">Praes tinci sed</p>
                        </div>

                    </div>
                    <hr>


                </div>
                <div class="four">
                    <div class="contain">
                        <div class="hi"><img src="./food_gallery/skies.jpg" alt="" srcset="" height="65px" width="60px">
                        </div>
                        <div class="hi">
                            <p class="two2">Dorum</p>
                            <p class="tt">Ultricies congue</p>
                        </div>

                    </div>
                    <hr>

                </div>
                <div class="five">
                    <div class="contain">
                        <div class="hi"><img src="./food_gallery/rock.jpg" alt="" srcset="" height="65px" width="60px">
                        </div>
                        <div class="hi">
                            <p class="two2">Mingsum</p>
                            <p class="tt">Lorem ipsum dipsum</p>
                        </div>

                    </div>
                    <hr>
                </div>

            </div>



        </div>
        <div class="box4">
            <img src="./food_gallery/bridge.jpg" alt="" width="855px" height="300px">
            <div class="inner">
                <h1 class="hi">BLOG ENTRY</h1>
                <p class="font_">Title description April 2,2024</p>
                <p class="font1"> Lorem ipsum, dolor sit amet consectetur adipisicing elit. Autem necessitatibus vitae
                    repellat exercitationem. Voluptas vitae tempore nisi nostrum consequatur eveniet neque impedit hic
                    tenetur qui minima commodi nobis magni distinctio modi debitis quod, minus maxime voluptate ea.
                    Cupiditate perferendis veritatis inventore animi iste praesentium aperiam, nisi at quidem doloribus
                    maxime!</p>

            </div>
            <div class="inner1">
                <div> <button class="button">Read More >></button></div>
                <div class="comm">
                    Comments
                    <span class="black">2</span>
                </div>
            </div>


        </div>
        <div class="box5">
            <div class="box55">
                <div class="five1">
                    <p class="lasst">Tags</p>
                </div>
                <div class="five2">

                    <span class="same1">Travel</span>
                    <span class="same">New York</span>
                    <div class="same">London</div>
                    <div class="same">IKEA</div>
                    <div class="same">NORWAY</div>
                    <div class="same">DIY</div>
                    <div class="same">Ideas</div>
                    <div class="same">Baby</div>
                    <div class="same">Family</div>
                    <div class="same">News</div>
                    <div class="same">Clothing</div>
                    <div class="same">Shopping</div>
                    <div class="same">Sports</div>
                    <div class="same">Games</div>
                    <div class="same">Volleyball</div>
                </div>

            </div>


        </div>

    </div>
    <div class="footer">
        <div class="foot">
            <div class="f1"><button class="button1">Previous </button>
            </div>
            <div class="f2"><button class="button2">Next >></button></div>

        </div>
        <p class="bot">Powered by Tushar Sharma</p></div>
        
    </div>    

</body>

</html>
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']