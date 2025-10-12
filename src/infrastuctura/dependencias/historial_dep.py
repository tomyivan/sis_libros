import src.app.historial_app as historial_app
import src.infrastuctura.repositorio.historial_rep as historial_rep
import src.infrastuctura.http.historial.historial_ctl as historial_ctl
historialRep = historial_rep.HistorialRepositorio()
historialApp = historial_app.HistoriaApp( historialRep )
historialCtl = historial_ctl.HistorialControlador( historialApp )