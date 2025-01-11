export default function wheather() {
    return (
        <div className="container my-5">
            <div className="mx-auto rounded border text-center text-white p-4"
                style={{
                    backgroundColor: "#3B5FAB", width: "400px"
                }}>
                <h2 className="">wheather Forecast</h2>
                <nav class="navbar bg-body-tertiary">
                    <div class="container-fluid">
                        <form class="d-flex" role="search">
                            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" />
                            <button class="btn btn-outline-success" type="submit">Search</button>
                        </form>
                    </div>
                </nav>
            </div>
        </div>
    )
}