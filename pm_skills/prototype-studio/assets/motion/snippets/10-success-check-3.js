const path = wrapper.querySelector("svg path");
   const len = Math.ceil(path.getTotalLength());
   path.style.strokeDasharray = String(len);
   path.style.strokeDashoffset = String(len);
