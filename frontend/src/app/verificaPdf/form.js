export default function Form() {
  return (
    <form>
      <div className="w- flex flex-col justify-center align-middle p-5 sm:p-40">
        <div className="">
          <label
            htmlFor="username"
            className="block text-sm font-medium leading-6 text-gray-900"
          >
            Codigo verificador
          </label>
          <div className="flex mt-2 rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600">
            <input
              type="text"
              name="username"
              id="username"
              autoComplete="username"
              className="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6 "
              placeholder="Nome para a assinatura"
            />
          </div>
        </div>

        <div className="mt-2">
          <label
            htmlFor="naosei"
            className="block text-sm font-medium leading-6 text-gray-900"
          >
            naosei
          </label>
          <div className="flex mt-2 rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600">
            <input
              type="text"
              name="naosei"
              id="naosei"
              autoComplete="naosei"
              className="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6"
              placeholder="Nome para a assinatura"
            />
          </div>
        </div>
        <h2 className="text-2xl font-bold leading-9 tracking-tight text-center mt-6 text-green-500 uppercase">O pdf verificado é válido</h2>
        <p className="text-center mt-6 text-xl">
          Baixe o PDF{" "}
          <span className="font-semibold leading-6 text-indigo-600 hover:text-indigo-500 cursor-pointer">
            clicando aqui
          </span>
        </p>

        <div className="mt-6 flex items-center justify-end gap-x-6">
          <button
            type="submit"
            className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >
            Verificar
          </button>
        </div>
      </div>
    </form>
  );
}
