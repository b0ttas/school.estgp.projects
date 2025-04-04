package edu.estgp.sdis;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Serializable;
import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.List;

public class CalendarClient implements EventCallback, Serializable {

    CalendarServer _calendarServer;

    public CalendarClient(String host, int port) throws RemoteException,
            NotBoundException {
        Registry registry = LocateRegistry.getRegistry(host, port);
        _calendarServer = (CalendarServer) (registry.lookup("calendarServer"));
    }

    public void run() {
        System.out.print("RMI Calendar Client\n"
                + "Available commands:\n"
                + "<users> is a comma separated list of strings\n"
                + "<date> is a date in this format dd-MM-yyyy HH:mm:ss\n\n"

                + "add: <name>;<users>;<date> - to add an event\n"//ok
                + "remove: <id> - to remove an event\n"//ok
                + "update: <id>;<name>;<users>;<date> - to modify an event\n"//ok
                + "list: <user> - show all events for a user\n" //ok
                + "next: <user> - get next event for user\n" //nok
                + "register: <user> - register for upcoming events\n" //ok
                + "unregister - unregister from event notifications\n" //nok, it adds notifications

                + "quit - to close the client\n\n");

        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        try {
            while (true) {

                String line = br.readLine();

                try {
                    if (line.startsWith("add:")) {
                        // Add a new event
                        String params[] = getParameters(line, 3);
                        long id = _calendarServer.addEvent(parseEvent(
                                params[0], params[1], params[2]));
                        System.out.println("Event created with id: " + id);

                    } else if (line.startsWith("update:")) {
                        // Update an event
                        String params[] = getParameters(line, 4);
                        boolean success = _calendarServer.updateEvent((new Long(params[0])).longValue(), parseEvent(params[1], params[2], params[3]));

                        if (success) {
                            System.out.println("Event updated.");
                        } else {
                            System.out.println("Can't update the event.");
                        }

                    } else if (line.startsWith("remove:")) {
                        // Remove an event
                        String params[] = getParameters(line, 1);
                        boolean success = _calendarServer
                                .removeEvent((new Long(params[0])).longValue());

                        if (success) {
                            System.out.println("Event removed.");
                        } else {
                            System.out.println("Can't remove the event.");
                        }

                    } else if (line.startsWith("list:")) {
                        String params[] = getParameters(line, 1);
                        List<Event> events = _calendarServer.listEvents(params[0]);
                        if (events.isEmpty()) {
                            System.out.println("No entries.");
                        } else {
                            for (Event event : events) {
                                System.out.println(event);
                            }
                        }

                    } else if (line.startsWith("next:")) {
                        String params[] = getParameters(line, 1);
                        List<Event> events = _calendarServer.listEvents(params[0]);
                        if (events.isEmpty()) {
                            System.out.println("No entries.");
                        } else {
                            for (Event event : events) { //count events to come
                                System.out.println(event);
                            }
                        }

                    } else if (line.startsWith("register:")) {
                        String params[] = getParameters(line, 1);
                        _calendarServer.RegisterCallback(this, params[0]);

                    } else if (line.startsWith("unregister")) {
                        _calendarServer.UnregisterCallback(this);

                    } else if (line.equals("quit")) {
                        break;

                    } else {
                        System.err.println("Unknown command.");
                    }
                } catch (ParseException e) {
                    System.err.println("Invalid date format.");

                } catch (IllegalArgumentException e) {
                    System.err.println("Invalid arguments.");
                }
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Unregister from all callbacks
        try {
            _calendarServer.UnregisterCallback(this);
        } catch (RemoteException e) {
            System.err.println("Can't unregister from callbacks");
        }

        System.out.println("Connection Closed.");
    }

    /**
     * Parse an event from strings
     */

    public Event parseEvent(String name, String user, String date)
            throws ParseException {

        String[] users = user.split(",");

        Calendar calendar = Calendar.getInstance();
        SimpleDateFormat sdf = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");
        calendar.setTime(sdf.parse(date));

        return new Event(name, users, calendar.getTime());

    }

    /**
     * Parse list of parameters from string
     */
    public String[] getParameters(String line, int length)
            throws IllegalArgumentException {
        String[] parts = line.split(": ");
        if (parts.length == 2) {
            String[] params = parts[1].split(";");
            if (params.length == length) {
                return params;
            }
        }

        throw new IllegalArgumentException();
    }

    /**
     * Callable from server, if registered event happens
     */
    public void call(Event e) throws RemoteException {
        System.out.println("Notification from server");
        System.out.println(e);
    }

}
