import { initializeApp } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-analytics.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-auth.js";


const firebaseConfig = {
  apiKey: "AIzaSyDjPKQyFAufmVd-ap1rlmYfeq53zvqH5Z4",
  authDomain: "gatsu-fbddf.firebaseapp.com",
  databaseURL: "https://gatsu-fbddf-default-rtdb.firebaseio.com",
  projectId: "gatsu-fbddf",
  storageBucket: "gatsu-fbddf.appspot.com",
  messagingSenderId: "330110714731",
  appId: "1:330110714731:web:222876623105373d21c22e"
};

const mp = new MercadoPago('TEST-9378860e-754e-4844-960e-1ce0855a2411');
const bricksBuilder = mp.bricks();

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth();

export class ManageAccount {
register(email, password) {
  createUserWithEmailAndPassword(auth, email, password)
    .then((_) => {
      window.location.href = "{% url 'Home' %}";
      // Mostrar alerta de registro exitoso
      alert("Registro exitoso. Serás redirigido a la página de inicio de sesión.");
    })
    .catch((error) => {
      console.error(error.message);
          // Mostrar alerta de error de registro
          alert("Error al registrar: " + error.message);
    });
}

authenticate(email, password) {
  signInWithEmailAndPassword(auth, email, password)
    .then((_) => {
      window.location.href = "{% url 'Home' %}";
      // Mostrar alerta de inicio de sesión exitoso
      alert("Has iniciado sesión correctamente. Serás redirigido a la página principal.");
    })
    .catch((error) => {
      console.error(error.message);
              // Mostrar alerta de error de inicio de sesión
              alert("Error al iniciar sesión: " + error.message);
    });
}

signOut() {
  signOut(auth)
    .then((_) => {
      window.location.href = "{% url 'Home' %}";
    })
    .catch((error) => {
      console.error(error.message);
    });
}
}
  console.log('Holaaaaa')


  var TrandingSlider = new Swiper('.tranding-slider', {
    effect: 'coverflow',
    grabCursor: true,
    centeredSlides: true,
    loop: true,
    slidesPerView: 'auto',
    coverflowEffect: {
      rotate: 0,
      stretch: 0,
      depth: 100,
      modifier: 2.5,
    },
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    }
  });
  console.log('Hola')
  

  document.getElementById("login-form").addEventListener("submit", (event) => {
    event.preventDefault();
  
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;
  
    const account = new ManageAccount();
    account.authenticate(email, password);
    
  });
  
  console.log('login-form');
  
  document.getElementById("signup-form").addEventListener("submit", (event) => {
    event.preventDefault();
  
    const email = document.getElementById("signup-email").value;
    const password = document.getElementById("signup-password").value;
  
    const account = new ManageAccount();
    account.register(email, password);
  
  });
  
  console.log('signup-form');

            /*
           Brick de mercadopago.
          */
  const renderCardPaymentBrick = async (bricksBuilder) => {
    const settings = {
      initialization: {
        amount: 4000, // monto total a pagar
      },
      callbacks: {
        onReady: () => {
          /*
            Callback llamado cuando Brick está listo.
            Aquí puedes ocultar cargamentos de su sitio, por ejemplo.
          */
        },
        onSubmit: (formData) => {
          // callback llamado al hacer clic en el botón enviar datos
          return new Promise((resolve, reject) => {
            fetch('/process_payment', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(formData),
            })
              .then((response) => response.json())
              .then((response) => {
                // recibir el resultado del pago
                resolve();
              })
              .catch((error) => {
                // manejar la respuesta de error al intentar crear el pago
                reject();
              });
          });
        },
        onError: (error) => {
          // callback llamado para todos los casos de error de Brick
          console.error(error);
        },
      },
     };
     window.cardPaymentBrickController = await bricksBuilder.create(
      'cardPayment',
      'cardPaymentBrick_container',
      settings,
     );  
   };
   renderCardPaymentBrick(bricksBuilder);
