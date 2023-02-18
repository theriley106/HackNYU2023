from flask import Flask, redirect, request, render_template
import os
import sys

@app.route("/")
def home():
    return render_template("index.html")

