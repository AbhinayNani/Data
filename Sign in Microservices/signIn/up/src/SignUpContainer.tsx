import { useFormik } from "formik";
// import React from "react";
import { FaFacebook, FaGoogle, FaTwitter } from "react-icons/fa";

interface SignUpValues {
  email: string;
  password: string;
  name: string;
}

async function submitData(endpoint: string, data: SignUpValues) {
  try {
    const response = await fetch(`http://localhost:9200/${endpoint}`, {
      method: "POST",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
      redirect: "follow",
      referrerPolicy: "no-referrer",
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      if (response.status === 409) {
        throw new Error("User with this email already exists");
      }
      throw new Error("Failed to submit data");
    }

    const result = await response.json();
    console.log(result);
    alert("User registered successfully!");
  } catch (error:any) {
    console.error("Error submitting data:", error);
    alert(error.message);
  }
}

function SignUpForm() {
  const validate = (values: SignUpValues) => {
    const errors: Partial<SignUpValues> = {};
    if (!values.email) {
      errors.email = "Required";
    } else if (
      !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)
    ) {
      errors.email = "Invalid email address";
    }

    if (!values.password) {
      errors.password = "*Required";
    } else if (
      !/(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*/i.test(
        values.password
      )
    ) {
      errors.password =
        "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, and one special character.";
    }
    if (errors.email === "" && errors.password === "") {
      alert("Entered {values.email} and password as {values.password}");
    }
    if (!values.name) {
      errors.name = "*Required";
    }
    return errors;
  };
  const formik = useFormik<SignUpValues>({
    initialValues: {
      email: "",
      password: "",
      name: "",
    },
    validate,
    onSubmit: async(values,{ setSubmitting }) => {
      console.log(values);
      await submitData("signup",values);
      setSubmitting(false);
      alert(JSON.stringify(values, null, 2));
      formik.resetForm();
    },
  });
  // const handleChange = (evt: { target: { value: unknown; name: string; }; }) => {
  //   const value = evt.target.value;
  //   setState({
  //     ...state,
  //     [evt.target.name]: value
  //   });
  // };

  // const handleOnSubmit = (evt: { preventDefault: () => void; }) => {
  //   evt.preventDefault();

  //   const { name, email, password } = state;
  //   alert(
  //     `You are sign up with name: ${name} email: ${email} and password: ${password}`
  //   );

  //   for (const key in state) {
  //     setState({
  //       ...state,
  //       [key]: ""
  //     });
  //   }
  // };

  return (
    <div className="form-container sign-up-container">
      <form onSubmit={formik.handleSubmit}>
        <h1>Create Account</h1>
        <div className="social-container">
          <a href="#" className="social">
            {/* <i className="fab fa-facebook-f" /> */}
            <FaFacebook />
          </a>
          <a href="#" className="social">
            {/* <i className="fab fa-google-plus-g" /> */}
            <FaGoogle />
          </a>
          <a href="#" className="social">
            {/* <i className="fab fa-linkedin-in" /> */}
            <FaTwitter />
          </a>
        </div>
        <span>or use your email for registration</span>
        <input
          type="text"
          name="name"
          value={formik.values.name}
          onChange={formik.handleChange}
          placeholder="Name"
          onBlur={formik.handleBlur}
        />
        {formik.touched.name && formik.errors.name ? (
          <span
            style={{
              color: "red",
              alignSelf: "self-start",
              marginLeft: "2em",
              marginTop: "-0.5em",
            }}
          >
            {formik.errors.name}
          </span>
        ) : null}
        <input
          type="email"
          name="email"
          placeholder="Email"
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          value={formik.values.email}
        />
        {formik.touched.email && formik.errors.email ? (
          <span
            style={{
              color: "red",
              alignSelf: "self-start",
              marginLeft: "2em",
              marginTop: "-0.5em",
            }}
          >
            {formik.errors.email}
          </span>
        ) : null}
        <input
          type="password"
          name="password"
          placeholder="Password"
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          value={formik.values.password}
        />
        {formik.touched.password && formik.errors.password ? (
          <span
            style={{
              color: "red",
              alignSelf: "self-start",
              marginLeft: "2em",
              marginTop: "-0.5em",
            }}
          >
            {formik.errors.password}
          </span>
        ) : null}
        <button>Sign Up</button>
      </form>
    </div>
  );
}

export default SignUpForm;
