# Adv Auto Filter Bot V2

<p align="center">
  <a href="https://github.com/AlbertEinsteinTG/Adv-Auto-Filter-Bot-V2/stargazers">
    <img src="https://img.shields.io/github/stars/AlbertEinsteinTG/Adv-Auto-Filter-Bot-V2?style=social">

  </a>
  
  <a href="https://github.com/AlbertEinsteinTG/Adv-Auto-Filter-Bot-V2/fork">
    <img src="https://img.shields.io/github/forks/AlbertEinsteinTG/Adv-Auto-Filter-Bot-V2?label=Fork&style=social">

  </a>  
</p>

__This Is Just An Simple Advance Auto Filter Bot Complete Rewritten Version Of [Adv-Filter-Bot](https://github.com/AlbertEinsteinTG/Adv-Auto-Filter-Bot)..__

__Just Sent Any Text As Query It Will Search For All Connected Chat's Files In Its MongoDB And Reply You With The Message Link As A Button__


## Usage

**__How To Use Me!?__**

* -> Add me to any group and make me admin<br>
* -> Add me to your channel as admin with full previlages

**Bot Commands (Works Only In Groups) :**


  * -> `/add chat_id`<br>
     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
OR
     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- To establish a connection of group with a channel (Bot should be admin with full previlages in both group and channel)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`/add @Username`


  * -> `/del chat_id`<br>
     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
OR 
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- To delete a group's coneection with a channel (Use disable option from settigns pannel for disconnecting temporarily instead of deleteing)<br>
    &nbsp;&nbsp;&nbsp;&nbsp; `/del @Username`


  * -> `/delall`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - To delete all connections of a group and deletes all its file from DB
  
  * -> `/settings`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -  To disaply a Settings Pannel Instance which can be used to tweek bot's settings accordingly

    * -> Channel - Button will show you all the connected chats with the group along with there index buttons correspnding to there order for furthur controls...

    * -> Filter Types - Button will show you the 3 filter types available in bot... Pressing each buttons will either enable or disable them and this will take into action as soon as you use them...without the need of a restart....

    * -> Configure - Button will help you to change no. of pages/ buttons per page/ total result without acutally editing the repo... Also it provide option to Enable/Disable  showing Invite Link in each results

    * -> Status - Button will show the stats of your current group

### Pre Requisites 
------------------
* ->__Your Bot Token From [@BotFather](http://www.telegram.dog/BotFather)__

* ->__Your APP ID And API Harsh From [Telegram](http://www.my.telegram.org) or [@UseTGXBot](http://www.telegram.dog/UseTGXBot)__

* ->__Your User Session String Obtained From [@PyrogramStringBot](http://www.telegram.dog/PyrogramStringBot)__

* ->__Mongo DB URL Obtained From [Mongo DB](http://www.mongodb.com)__

#### PR's Are Very Welcome

## Deploy
You can deploy this bot anywhere.

<i>**[Watch Deploying Tutorial...](https://youtu.be/KTearEPhumc)**</i>

<details><summary>Deploy To Heroku</summary>
<p>
<br>
<a href="https://heroku.com/deploy?template=https://github.com/AlbertEinsteinTG/Adv-Auto-Filter-Bot-V2/tree/main">
  <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy">
</a>
</p>
</details>

<details><summary>Deploy To VPS</summary>
<p>
<pre>
git clone https://github.com/AlbertEinsteinTG/Adv-Auto-Filter-Bot-V2
cd Adv-Auto-Filter-Bot-V2
pip3 install -r requirements.txt
# Change The Vars Of bot/__init__.py File Accordingly
python3 -m bot
</pre>
</p>
</details>

## Support   
Join Our [Telegram Group](https://www.telegram.dog/CrazyBotszGrp) For Support/Assistance And Our [Channel](https://www.telegram.dog/CrazyBotsz) For Updates.   
   
Report Bugs, Give Feature Requests There..   
Do Fork And Star The Repository If You Liked It.

## Disclaimer
[![GNU Affero General Public License v3.0](https://www.gnu.org/graphics/agplv3-155x51.png)](https://www.gnu.org/licenses/agpl-3.0.en.html#header)    
Licensed under [GNU AGPL v3.0.](https://github.com/AlbertEinsteinTG/Adv-Auto-Filter-Bot-V2/blob/main/LICENSE)
Selling The Codes To Other People For Money Is *Strictly Prohibited*.


## Credits

 - Thanks To Dan For His Awsome [Libary](https://github.com/pyrogram/pyrogram)
 - Thanks To SpEcHiDe For His Awesome [DeleteMessagesRoBot](https://github.com/SpEcHiDe/DeleteMessagesRoBot)
