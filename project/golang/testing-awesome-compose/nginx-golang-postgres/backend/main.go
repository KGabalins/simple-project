package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"text/template"
	"time"

	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
	_ "github.com/lib/pq"
)

var tpl *template.Template

func init() {
	tpl = template.Must(template.ParseGlob("templates/*htm"))
}

func connect() (*sql.DB, error) {
	bin, err := ioutil.ReadFile("/run/secrets/db-password")
	if err != nil {
		return nil, err
	}
	return sql.Open("postgres", fmt.Sprintf("postgres://postgres:%s@db:5432/example?sslmode=disable", string(bin)))
}

func indexHandler(w http.ResponseWriter, r *http.Request) {
	tpl.ExecuteTemplate(w, "index.htm", nil)
}

func blogHandler(w http.ResponseWriter, r *http.Request) {
	db, err := connect()
	if err != nil {
		w.WriteHeader(500)
		return
	}
	defer db.Close()

	rows, err := db.Query("SELECT title FROM blog")
	if err != nil {
		w.WriteHeader(500)
		return
	}
	var titles []string
	for rows.Next() {
		var title string
		err = rows.Scan(&title)
		titles = append(titles, title)
	}
	json.NewEncoder(w).Encode(titles)
}

func appleHandler(w http.ResponseWriter, r *http.Request) {
	db, err := connect()
	if err != nil {
		w.WriteHeader(500)
		return
	}
	defer db.Close()

	rows, err := db.Query("SELECT title FROM apples")
	if err != nil {
		w.WriteHeader(500)
		return
	}
	var titles []string
	for rows.Next() {
		var title string
		err = rows.Scan(&title)
		titles = append(titles, title)
	}
	json.NewEncoder(w).Encode(titles)
}

func helloHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "Hello World!")
}

func processHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Redirect(w, r, "/index", http.StatusSeeOther)
		return
	}

	fname := r.FormValue("firstname")
	lname := r.FormValue("lastname")

	d := struct {
		First string
		Last  string
	}{
		First: fname,
		Last:  lname,
	}

	tpl.ExecuteTemplate(w, "processor.htm", d)
}

func main() {
	log.Print("Prepare db...")
	if err := prepare(); err != nil {
		log.Fatal(err)
	}

	log.Print("Listening 8000")
	r := mux.NewRouter()
	r.HandleFunc("/", blogHandler)
	r.HandleFunc("/hello", helloHandler)
	r.HandleFunc("/apples", appleHandler)
	r.HandleFunc("/process", processHandler)
	r.HandleFunc("/index", indexHandler)
	log.Fatal(http.ListenAndServe(":8000", handlers.LoggingHandler(os.Stdout, r)))
}

func prepare() error {
	db, err := connect()
	if err != nil {
		return err
	}
	defer db.Close()

	for i := 0; i < 60; i++ {
		if err := db.Ping(); err == nil {
			break
		}
		time.Sleep(time.Second)
	}

	if _, err := db.Exec("DROP TABLE IF EXISTS blog"); err != nil {
		return err
	}

	if _, err := db.Exec("CREATE TABLE IF NOT EXISTS blog (id SERIAL, title VARCHAR)"); err != nil {
		return err
	}

	for i := 0; i < 5; i++ {
		if _, err := db.Exec("INSERT INTO blog (title) VALUES ($1);", fmt.Sprintf("Blog post #%d", i)); err != nil {
			return err
		}
	}

	if _, err := db.Exec("DROP TABLE IF EXISTS apples"); err != nil {
		return err
	}

	if _, err := db.Exec("CREATE TABLE IF NOT EXISTS apples (id SERIAL, title VARCHAR)"); err != nil {
		return err
	}

	for i := 0; i <= 5; i++ {
		if _, err := db.Exec("INSERT INTO apples (title) VALUES ($1);", fmt.Sprintf("Apple number #%d", i)); err != nil {
			return err
		}
	}
	return nil
}
