import React, { useContext } from "react";
import { Context } from "../store/appContext";
import { SignupForm } from "../component/signup-form";


export const Signup = () => {
	const { store, actions } = useContext(Context);

	return (
		<div className="text-center mt-5">
			<h1>Signup</h1>
			<SignupForm />
		</div>
	);
};
