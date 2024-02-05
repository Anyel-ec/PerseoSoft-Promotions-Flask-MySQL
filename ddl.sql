create database promociones;

use promociones;
drop table if exists Productos;
CREATE TABLE Productos (
    ProductoID INT PRIMARY KEY AUTO_INCREMENT,
    CodigoBarras VARCHAR(50) UNIQUE,
    Nombre VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    Precio DECIMAL(10, 2) NOT NULL
);

-- Insertar productos
INSERT INTO Productos (CodigoBarras, Nombre, Descripcion, Precio)
VALUES
('1234567890123', 'Refresco', 'Bebida carbonatada', 1.99),
('2345678901234', 'Pan', 'Pan fresco de trigo', 2.50),
('3456789012345', 'Azúcar', 'Azúcar refinada', 1.00),
('4567890123456', 'Café', 'Café molido', 5.99);


drop table if exists DosxUno;

CREATE TABLE DosxUno(
    PromocionID INT PRIMARY KEY AUTO_INCREMENT,
    codigoPromocion VARCHAR(50) UNIQUE,
    Nombre VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    FechaInicio DATE NOT NULL,
    FechaFin DATE NOT NULL
);

-- Insertar promociones
INSERT INTO DosxUno (codigoPromocion, Nombre, Descripcion, FechaInicio, FechaFin)
VALUES
('PROMOO1', 'Promo Pan y Refresco', '2x1', '2024-02-01', '2024-02-28'),
('PROMOO2', 'Promo Combo Café', '3x1', '2024-03-01', '2024-03-31');
select * from DosxUno;


drop table if exists Productos_Promocion;

CREATE TABLE Productos_Promocion (
    AsociacionID INT PRIMARY KEY AUTO_INCREMENT,
    PromocionID INT,
    ProductoID INT,
    FOREIGN KEY (PromocionID) REFERENCES DosxUno(PromocionID),
    FOREIGN KEY (ProductoID) REFERENCES Productos(ProductoID)
);

-- Asociar productos a las promociones
INSERT INTO Productos_Promocion (PromocionID, ProductoID)
VALUES
(1, 1), -- Asociar Refresco a Promo Pan y Refresco
(1, 2), -- Asociar Pan a Promo Pan y Refresco
(2, 2), -- Asociar Pan a Promo Combo Café
(2, 3), -- Asociar Azúcar a Promo Combo Café
(2, 4); -- Asociar Café a Promo Combo Café





SELECT
    P.ProductoID,
    P.Nombre AS NombreProducto,
    P.Descripcion AS DescripcionProducto,
    P.Precio,
    D.PromocionID,
    D.Nombre AS NombrePromocion,
    D.Descripcion AS DescripcionPromocion,
    D.FechaInicio,
    D.FechaFin
FROM Productos AS P
JOIN Productos_Promocion AS PP ON P.ProductoID = PP.ProductoID
JOIN DosxUno AS D ON PP.PromocionID = D.PromocionID;


