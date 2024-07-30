import React, { Component } from "react";
import { Link } from "react-router-dom";


export const Footer = () => (
	<footer className="footer mt-auto py-3 text-center">
		<p><Link to="/signup"><button type="button" className="btn btn-link">Sign Up</button></Link></p>
		<p>
			Made with <i className="fa fa-heart text-success" /> by{" "}
			<a href="www.linkedin.com/in/agustin-soto-holt">agusotoholt</a>
		</p>
	</footer>
);
