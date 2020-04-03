<h1><b>Sequel Injector <span style="color:#22d8dd ">&#129302;</span> </b></h1>

<p>
    An automated tool that autopopulates the database from entries in a table image, based on OpenCV and PyTesseract.
</p>
<br>
<h2>Dependencies</h2>
<p>Based on <code>python 3.6+</code>.</p>
<p>Run <code>pip install -r requirements.txt</code> to install all dependencies.</p>
<h2>How to setup?</h2>
<p><b>Create a virtual environment:</b></p>
<ul>
    <li>Installing <b>virtualenv</b> : <code>pip3 install virtualenv</code>
    </li>
    <li>Creating <b>venv</b>: <code>python -m venv env</code></li>
    <li>Activating <b>env</b>: <code>source env/bin/activate</code></li>
</ul>
<p>Install all dependencies.</p>
<p>Set up <code>config.js</code> by copying contents of <code>config.example.json</code> to <code>config.json</code> and fill in username and password of your database client.</p>

<h2>Arguments</h2>
<ul>
    <li><code>-p/ --path</code>: Path of the image to be processed</li>
    <li><code>-db/ --database</code>: Name of the database</li>
    <li><code>-t/ --table</code>: Name of the table</li>
</ul>
<h2>Executing the script:</h2>
<p>Run <code>python injector.py</code> with respective arguments.</p>

<h3>=====================<br>Have Fun <br>=====================</h3>
