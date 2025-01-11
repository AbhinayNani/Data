import { FaFacebook, FaGoogle, FaTwitter } from "react-icons/fa";
import { useFormik } from "formik";
import { useNavigate } from "react-router-dom";

interface SignInValues {
  email: string;
  password: string;
}

async function submitData(endpoint: string, data: SignInValues) {
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
      } else if (response.status === 401) {
        throw new Error("Invalid email or password");
      } else {
        throw new Error("Failed to submit data");
      }
    } else {
      const result = await response.json();
      // alert(
      //   "Operation successful: " +
      //     (result.message || "User registered successfully!")
      // );
      return true;
    }
  } catch (error: any) {
    console.error("Error submitting data:", error);
    alert(error.message);
  }
}

function SignInForm() {
  const navigate = useNavigate();
  const validate = (values: SignInValues) => {
    const errors: Partial<SignInValues> = {};

    if (!values.email) {
      errors.email = "*Required";
    } else if (
      !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)
    ) {
      errors.email = "*Invalid email address";
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

    return errors;
  };

  const formik = useFormik<SignInValues>({
    initialValues: {
      email: "",
      password: "",
    },
    validate,
    onSubmit: async (values, { setSubmitting }) => {
      try {
        const k=await submitData("signin", values);
        if (k) {
          console.log("asdfghjkl");
          localStorage.setItem("user", JSON.stringify(values));
          console.log(values);
          
          navigate("/Home");
        }
      } catch (e: any) {
        alert(e.message);
      } finally {
        setSubmitting(false);
        formik.resetForm();
      }
    },
  });

  return (
    <div className="form-container sign-in-container">
      <form onSubmit={formik.handleSubmit}>
        <h1>Sign in</h1>
        <div className="social-container">
          <a href="#" className="social">
            <FaFacebook />
          </a>
          <a href="#" className="social">
            <FaGoogle />
          </a>
          <a href="#" className="social">
            <FaTwitter />
          </a>
        </div>
        <span>or use your account</span>
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
        <a href="#">Forgot your password?</a>
        <button type="submit">Sign In</button>
      </form>
    </div>
  );
}

export default SignInForm;
